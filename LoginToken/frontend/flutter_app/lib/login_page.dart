import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';


class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();

  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  String? _errorMessage;

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submitLogin() async {
    setState(() {
      _errorMessage = null;
    });

    if (_formKey.currentState!.validate()) {
      final username = _usernameController.text;
      final password = _passwordController.text;

      try {
        final url = const String.fromEnvironment('BACKEND_ENDPOINT') + '/user-manager/login';
        final response = await http.post(
          Uri.parse(url),
          headers: {'Content-Type': 'application/json'},
          body: json.encode({
            'username': username,
            'password': password,
          }),
        );

        if (response.statusCode == 200) {
          final responseData = jsonDecode(response.body);
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('access_token', responseData['access_token']);
          if (responseData.containsKey('refresh_token')) {
            await prefs.setString('refresh_token', responseData['refresh_token']);
          }
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('로그인 성공! ${responseData}')),
          );
          final tabController = DefaultTabController.of(context);
          if (tabController != null) {
            tabController.animateTo(0);
          }
        } else if (response.statusCode == 401) {
          setState(() {
            _errorMessage = '아이디 또는 비밀번호가 올바르지 않습니다.';
          });
        } else {
          setState(() {
            _errorMessage = '로그인에 실패했습니다. 다시 시도해주세요.';
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
              '로그인',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),

            if (_errorMessage != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 12.0),
                child: Text(
                  _errorMessage!,
                  style: const TextStyle(color: Colors.red),
                  textAlign: TextAlign.center,
                ),
              ),

            TextFormField(
              controller: _usernameController,
              decoration: const InputDecoration(labelText: '사용자 이름'),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return '사용자 이름을 입력하세요.';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: '비밀번호'),
              obscureText: true,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return '비밀번호를 입력하세요.';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _submitLogin,
              child: const Text('로그인'),
            ),
          ],
        ),
      ),
    );
  }
}

