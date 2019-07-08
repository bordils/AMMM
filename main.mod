/*********************************************
 * OPL 12.8.0.0 Model
 * Author: Miguel y Elena
 * Creation Date: 22/10/2018 at 10:57:19
 *********************************************/
 
 main {
	var src = new IloOplModelSource("AMMM Project.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def,cplex);
	var data = new IloOplDataSource("p1.dat");
	model.addDataSource(data);
	model.generate();
	cplex.epgap=1;
	//cplex.tilim = 60*60;
	if (cplex.solve()) {	
		writeln("Cost " + cplex.getObjValue() + "€");
		writeln("x_ds"+model.x_ds);
		writeln("x_bs"+model.x_bs);
		writeln("ed"+model.ed);
	}else {
		writeln("Not solution found");
	}	
	model.end();
	data.end();
	def.end();
	cplex.end();
	src.end();
};