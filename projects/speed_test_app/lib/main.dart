import 'dart:math';
import 'package:flutter/material.dart';
void main(){
  runApp(MaterialApp(
      title:'反应速度测试器',
      theme: ThemeData(primarySwatch:Colors.cyan),
      home:SpeedTestApp()
    ));
}
Future<int> randomWait(){
  int second = (Random().nextInt(4))+1;
  return Future.delayed(Duration(seconds:second),()=>second);
}
class SpeedTestApp extends StatefulWidget{
  const SpeedTestApp({super.key});
  @override
  State<SpeedTestApp> createState() => SpeedTestAppState();
}
class SpeedTestAppState extends State<SpeedTestApp>{
  bool readyState=true;
  bool waiting = false;
  int time = -1;
  int? wait;
  int start = -1;
  void pressProcess() async{
    if(readyState){
      setState((){
        readyState=false;
      });
      start = DateTime.now().millisecondsSinceEpoch;
      setState((){
        waiting=true;
      });
      wait = await randomWait();
      setState((){
        waiting=false;
      });
    }else{
      if(!waiting){
        setState((){
          time=DateTime.now().millisecondsSinceEpoch-start-(wait!*1000);
          readyState=true;
        });
      }
    }
  }
  @override
  Widget build(BuildContext context) {
    Color c =((!readyState)&&(!waiting))?Colors.red:Colors.blue;
    return Scaffold(
      backgroundColor: c,
      appBar: AppBar(
        title: const Text('反应速度测试器')
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children:<Widget>[
            SizedBox(height:20),
            Text(
              '当页面变红时，立刻按下下方按钮',
              style:TextStyle(
                color:Colors.amber,
              )
            ),
            SizedBox(height:20),
            ElevatedButton(
              onPressed:pressProcess,
              child:Text('按钮'),
            ),
            SizedBox(height:20),
            Text(
              (readyState&&(time!=-1)?'反应时间：${time}ms':''),
              style:TextStyle(
                color:Colors.red
              )
            )
          ]
        )
      )
    );
  }
}