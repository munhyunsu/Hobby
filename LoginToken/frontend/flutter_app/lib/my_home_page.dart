import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:cookie_jar/cookie_jar.dart';
import 'package:dio_cookie_manager/dio_cookie_manager.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Timer? _timer;
  String? _username;
  int? _exp;
  int? _refreshExp;
  int _now = DateTime.now().toUtc().millisecondsSinceEpoch ~/ 1000;
  bool _isHealthy = true;

  late final Dio _dio;
  final CookieJar _cookieJar = CookieJar();

  @override
  void initState() {
    super.initState();
    _setupDio();
    _loadTokenInfo();
    _startCountdownTimer();
  }

  void _setupDio() {
    _dio = Dio(BaseOptions(
      baseUrl: const String.fromEnvironment('BACKEND_ENDPOINT'),
      headers: {'Content-Type': 'application/json'},
    ));
    if (!kIsWeb) {
      _dio.interceptors.add(CookieManager(_cookieJar));
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _startCountdownTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (_) async {
      setState(() {
        _now = DateTime.now().toUtc().millisecondsSinceEpoch ~/ 1000;
      });

      if (_exp != null && _exp! - _now < 30) {
        await _checkHealthAndRefresh();
        await _checkHealthAndRefresh();
      }

      if (_refreshExp != null && _refreshExp! <= _now) {
        await _logout();
      }
    });
  }

  Future<void> _loadTokenInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) return;

    try {
      final response = await _dio.get('/token-manager/token/decode',
          options: Options(headers: {'Authorization': 'Bearer $token'}, extra: {'withCredentials': true}));
      final data = response.data;
      final access = data['access_token'];
      final refresh = data['refresh_token'];

      setState(() {
        _username = access['sub'];
        _exp = (access['exp'] as num).toInt();
        _refreshExp = (refresh['exp'] as num).toInt();
      });
    } catch (_) {}
  }

  Future<void> _checkHealthAndRefresh() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) return;

    try {
      final response = await _dio.get('/token-manager/is-healthy',
          options: Options(headers: {'Authorization': 'Bearer $token'}, extra: {'withCredentials': true}));
      final data = response.data;
      final access = data['access_token'];
      final refresh = data['refresh_token'];

      final accessHealthy = access['is_healthy'] as bool;
      final refreshHealthy = refresh['is_healthy'] as bool;

      setState(() => _isHealthy = accessHealthy);
      
      /*
      if (!accessHealthy) await _renewAccessToken();
      if (!refreshHealthy) {
        final success = await _renewRefreshToken();
        if (!success) await _logout();
      }
      */
      if (!accessHealthy) {
        final success = await _renewToken();
        if (!success) await _logout();
      }
    } catch (_) {}
  }

  Future<void> _renewAccessToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) return;

    try {
      final response = await _dio.post('/token-manager/renew/access_token',
          options: Options(headers: {'Authorization': 'Bearer $token'}, extra: {'withCredentials': true}));
      if (response.statusCode == 200) {
        final newToken = response.data['access_token'];
        await prefs.setString('access_token', newToken);
        await _loadTokenInfo();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Access token 자동 갱신됨')),
        );
      }
    } catch (_) {}
  }

  Future<bool> _renewRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) return false;

    try {
      final response = await _dio.post('/token-manager/renew/refresh_token',
          options: Options(headers: {'Authorization': 'Bearer $token'}, extra: {'withCredentials': true}));
      if (response.statusCode == 200) {
        final newToken = response.data['access_token'];
        await prefs.setString('access_token', newToken);
        await _loadTokenInfo();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Refresh token 자동 갱신됨')),
        );
        return true;
      }
    } catch (_) {}
    return false;
  }

  Future<bool> _renewToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) return false;

    try {
      final response = await _dio.post('/token-manager/renew/token',
          options: Options(headers: {'Authorization': 'Bearer $token'}, extra: {'withCredentials': true}));
      if (response.statusCode == 200) {
        final newToken = response.data['access_token'];
        await prefs.setString('access_token', newToken);
        await _loadTokenInfo();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Access token, Refresh token 자동 갱신됨')),
        );
        return true;
      }
    } catch (_) {}
    return false;
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();

    setState(() {
      _username = null;
      _exp = null;
      _refreshExp = null;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Refresh token이 만료되어 로그아웃되었습니다.')),
    );
  }

  String _formatExp(int? exp) {
    if (exp == null) return '-';
    final dt = DateTime.fromMillisecondsSinceEpoch(exp * 1000, isUtc: true).toLocal();
    return dt.toString();
  }

  int _remainingSeconds() {
    if (_exp == null) return 0;
    return (_exp! - _now).clamp(0, double.infinity).toInt();
  }

  int _remainingRefreshSeconds() {
    if (_refreshExp == null) return 0;
    return (_refreshExp! - _now).clamp(0, double.infinity).toInt();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('👤 사용자: ${_username ?? '불명'}', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 12),
            Text('⏰ Access token 만료 시간: ${_formatExp(_exp)}'),
            Text('⏳ Access token 남은 시간: ${_remainingSeconds()}초'),
            Text('🔁 Refresh token 만료 시간: ${_formatExp(_refreshExp)}'),
            Text('⏳ Refresh token 남은 시간: ${_remainingRefreshSeconds()}초'),
            const SizedBox(height: 12),
            Text(
              _isHealthy ? '✅ 상태: 정상 (Healthy)' : '⚠️ 상태: 갱신됨 (Unhealthy)',
              style: TextStyle(
                color: _isHealthy ? Colors.green : Colors.orange,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

