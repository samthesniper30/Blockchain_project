import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home:AddApp()));

class AddApp extends StatefulWidget{
    const AddApp({super.key});
    
    @override
    State <AddApp> createState() => _AddAppState();
}

class _AddAppState extends State<AddApp>{
    final a = TextEditingController();
    final b = TextEditingController();
    double sum = 0;

    @override
    Widget build(BuildContext context){
	return Scaffold(
	    appBar:AppBar(title: const Text('Add 2 numbers')),
	    body:Center(
		child:Column(
		    children:[
			TextField(controller:a,keyboardType:TextInputType.number),
			TextField(controller:b,keyboardType:TextInputType.number),
			ElevatedButton(
			    onPressed:() => setState(() => sum = double.parse(a.text) + double.parse(b.text)), child:const Text('add'),
			),
			Text('Result:$sum'),
		    ],
		),
	    ),
	);
    }
}


// import 'package:flutter/material.dart';

// void main() => runApp(const MaterialApp(home: ListApp()));

// class ListApp extends StatefulWidget {
//   const ListApp({super.key});

//   @override
//   State<ListApp> createState() => _ListAppState();
// }

// class _ListAppState extends State<ListApp> {
//   final itemController = TextEditingController();
//   final List<String> items = [];

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: const Text('Simple List Demo')),
//       body: Center(
//         child: Column(
//           children: [
//             TextField(
//               controller: itemController,
//               decoration: const InputDecoration(hintText: 'Enter item'),
//             ),
//             ElevatedButton(
//               onPressed: () {
//                 setState(() {
//                   items.add(itemController.text);
//                   itemController.clear();
//                 });
//               },
//               child: const Text('Add to list'),
//             ),
//             Expanded(
//               child: ListView.builder(
//                 itemCount: items.length,
//                 itemBuilder: (context, index) => ListTile(
//                   title: Text(items[index]),
//                 ),
//               ),
//             ),
//           ],
//         ),
//       ),
//     );
//   }
// }

