import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
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

  @override
  void initState() {
    super.initState();
    _loadTokenInfo();
    _startCountdownTimer();
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

    final url = const String.fromEnvironment('BACKEND_ENDPOINT') + '/user-manager/token/decode';
    final response = await http.get(
      Uri.parse(url),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final access = data['access_token'];
      final refresh = data['refresh_token'];
      final accessExp = access['exp'];
      final refreshExp = refresh['exp'];

      setState(() {
        _username = access['username'];
        _exp = accessExp is int ? accessExp : (accessExp as num).toInt();
        _refreshExp = refreshExp is int ? refreshExp : (refreshExp as num).toInt();
      });
    }
  }

  Future<void> _checkHealthAndRefresh() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) return;

    final url = const String.fromEnvironment('BACKEND_ENDPOINT') + '/user-manager/is-healthy';
    final response = await http.get(
      Uri.parse(url),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final healthy = data['is_healthy'] as bool;
      setState(() {
        _isHealthy = healthy;
      });

      if (!healthy) {
        await _renewAccessToken();
      }
    }
  }

  Future<void> _renewAccessToken() async {
    final url = const String.fromEnvironment('BACKEND_ENDPOINT') + '/user-manager/renew/access_token';
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) return;

    final response = await http.post(
      Uri.parse(url),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final newToken = data['access_token'];
      await prefs.setString('access_token', newToken);
      await _loadTokenInfo(); // 업데이트된 토큰으로 사용자 정보 및 만료 시간 갱신
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Access token 자동 갱신됨')),
      );
    }
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
            Text('⏳ Acress token 남은 시간: ${_remainingSeconds()}초'),
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

