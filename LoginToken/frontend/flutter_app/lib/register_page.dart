import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();

  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  String? _errorMessage;

  final _usernameRegExp = RegExp(r'^[a-zA-Z0-9_]+$');

  late final Dio _dio;

  @override
  void initState() {
    super.initState();
    _dio = Dio(BaseOptions(
      baseUrl: const String.fromEnvironment('BACKEND_ENDPOINT'),
      headers: {'Content-Type': 'application/json'},
    ));
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _submitForm() async {
    setState(() {
      _errorMessage = null;
    });

    if (_formKey.currentState!.validate()) {
      final username = _usernameController.text;
      final email = _emailController.text;
      final password = _passwordController.text;
      final confirmPassword = _confirmPasswordController.text;

      if (password != confirmPassword) {
        setState(() {
          _errorMessage = '비밀번호가 일치하지 않습니다.';
        });
        return;
      }

      try {
        final response = await _dio.post(
          '/user-manager/user',
          data: {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirmPassword,
          },
          options: Options(extra: {'withCredentials': true}),
        );

        if (response.statusCode == 200 || response.statusCode == 201) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('회원가입 완료!')),
          );
          final tabController = DefaultTabController.of(context);
          if (tabController != null) {
            tabController.animateTo(0);
          }
        }
      } on DioException catch (e) {
        if (e.response?.statusCode == 409) {
          setState(() {
            _errorMessage = '이미 사용 중인 사용자 이름 또는 이메일입니다.';
          });
        } else {
          setState(() {
            _errorMessage = '회원가입에 실패했습니다. 다시 시도해주세요.';
          });
        }
      } catch (e) {
        setState(() {
          _errorMessage = '서버에 연결할 수 없습니다.';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Form(
        key: _formKey,
        child: ListView(
          children: [
            const Text(
              '회원가입',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),

            if (_errorMessage != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 12.0),
                child: Text(
                  _errorMessage!,
                  style: const TextStyle(color: Colors.red, fontSize: 14),
                  textAlign: TextAlign.center,
                ),
              ),

            TextFormField(
              controller: _usernameController,
              decoration: const InputDecoration(labelText: '사용자 이름'),
              validator: (value) {
                if (value == null || value.length < 3) {
                  return '3자 이상 입력하세요.';
                }
                if (!_usernameRegExp.hasMatch(value)) {
                  return '영문자, 숫자, 밑줄만 사용할 수 있습니다.';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: '이메일'),
              keyboardType: TextInputType.emailAddress,
              validator: (value) {
                if (value == null || value.isEmpty || !value.contains('@')) {
                  return '올바른 이메일을 입력하세요.';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: '비밀번호'),
              obscureText: true,
              validator: (value) {
                if (value == null || value.length < 6) {
                  return '6자 이상 입력하세요.';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _confirmPasswordController,
              decoration: const InputDecoration(labelText: '비밀번호 확인'),
              obscureText: true,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return '비밀번호를 한 번 더 입력하세요.';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _submitForm,
              child: const Text('회원가입'),
            ),
          ],
        ),
      ),
    );
  }
}

