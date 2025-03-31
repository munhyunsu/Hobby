import 'package:flutter/material.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();

  String _email = '';
  String _password = '';
  String _confirmPassword = '';

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      if (_password != _confirmPassword) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('비밀번호가 일치하지 않습니다.')),
        );
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('회원가입 완료!')),
      );
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
            const SizedBox(height: 24),
            TextFormField(
              decoration: const InputDecoration(labelText: '이메일'),
              keyboardType: TextInputType.emailAddress,
              onSaved: (value) => _email = value ?? '',
              validator: (value) {
                if (value == null || value.isEmpty || !value.contains('@')) {
                  return '올바른 이메일을 입력하세요.';
                }
                return null;
              },
            ),
            TextFormField(
              decoration: const InputDecoration(labelText: '비밀번호'),
              obscureText: true,
              onSaved: (value) => _password = value ?? '',
              validator: (value) {
                if (value == null || value.length < 6) {
                  return '6자 이상 입력하세요.';
                }
                return null;
              },
            ),
            TextFormField(
              decoration: const InputDecoration(labelText: '비밀번호 확인'),
              obscureText: true,
              onSaved: (value) => _confirmPassword = value ?? '',
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

