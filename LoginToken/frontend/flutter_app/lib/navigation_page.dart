import 'package:flutter/material.dart';

import 'my_home_page.dart';


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
          bottom: const TabBar(
            tabs: [
              Tab(icon: Icon(Icons.home)),
              Tab(icon: Icon(Icons.app_registration)),
              Tab(icon: Icon(Icons.login)),
            ],
          ),
          title: Text(widget.title),
        ),
        body: const TabBarView(
          children: [
            MyHomePage(),
            Icon(Icons.app_registration),
            Icon(Icons.login),
          ],
        ),
      ),
    );
  }
}

