import 'package:flutter/material.dart';

import 'my_home_page.dart';
import 'register_page.dart';
import 'login_page.dart';


class NavigationPage extends StatefulWidget {
  const NavigationPage({super.key, required this.title});

  final String title;

  @override
  State<NavigationPage> createState() => _NavigationPageState();
}

class _NavigationPageState extends State<NavigationPage> {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          bottom: TabBar(
            tabs: [
              Tab(icon: Icon(Icons.home)),
              Tab(icon: Icon(Icons.app_registration)),
              Tab(icon: Icon(Icons.login)),
            ],
          ),
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          title: Text(widget.title),
        ),
        body: TabBarView(
          children: [
            MyHomePage(),
            RegisterPage(),
            LoginPage(),
          ],
        ),
      ),
    );
  }
}

