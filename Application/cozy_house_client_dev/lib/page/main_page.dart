import 'dart:convert';

import 'package:cozy_house_client_dev/common/navigator.dart';
import 'package:cozy_house_client_dev/page/history_page.dart';
import 'package:cozy_house_client_dev/page/security_page.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../utils/provider.dart';
import 'monitor_page.dart';

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Cozy House',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MainPage(),
    );
  }
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  // 탭 라벨 인덱스 - 초깃값 0
  int _selectedIndex = 0;
  String user_name = '';
  String user_email = '';

  @override
  void initState() {
    super.initState();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    loadProfileData();
  }

  loadProfileData() {
    // 앱 메모리에서 데이터 가져오기
    user_name = Provider.of<SharedPreferencesProvider>(context).getData('user_name')!;
    user_email = Provider.of<SharedPreferencesProvider>(context).getData('user_id')!;
  }

  @override
  Widget build(BuildContext context) {
    return CustomNavigator(
      titleText: _getSelectedTitle(),
      // 초기는 security page가 노출되고,
      selectedIndex: _selectedIndex,
      // 탭 이벤트가 발생하면 해당 탭의 인덱스로 화면을 조회하여 노출시킨다.
      onChanged: (index) {
        setState(() {
          _selectedIndex = index;
        });
      },
      user_name: user_name,
      user_email: user_email,
      pages: const [
        SecurityPage(),
        MonitorPage(),
        HistoryPage(),
      ],
    );
  }

  String _getSelectedTitle() {
    switch (_selectedIndex) {
      case 0:
        return 'Security';
      case 1:
        return 'Monitor';
      case 2:
        return 'Record';
      default:
        return 'Default';
    }
  }
}
