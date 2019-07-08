/*********************************************
 * OPL 12.8.0.0 Model
 * Author: Miguel y Elena
 * Creation Date: 22/10/2018 at 10:57:19
 *********************************************/
 
 
 
// basic variables: buses, drivers, services
int nBuses =...;
int nDrivers =...;
int nServices =...;
range B = 1..nBuses;
range D = 1..nDrivers;
range S = 1..nServices;

//datos de los autobuses
int maxBuses =...;
int bCap[b in B]=...;
float bCPM[b in B]=...;
float bCPKm[b in B]=...;

//datos de las rutas
float sStartTime[s in S]=...;
float sMin[s in S]=...;
float sKM[s in S]=...;
int sLoad[s in S]=...;

//datos conductores
float dMaxMin[d in D]=...;
float CBM =...;
float CEM =...;
int BM =...;

//matrices de decision conductores-servicios & buses-servicios
dvar boolean x_ds[d in D, s in S];
dvar boolean x_bs[b in B, s in S];
dvar boolean ed[d in D]; // decidir si el conductor trabaja
dvar boolean x_used[b in B]; //0 if bus is not used, 1 is bus is used

//funcion objetivo
dvar float+ cost;

execute
{
	var totalMinReq;
	var totalMinAvail;
	for (var s=1;s<=nServices;s++)
	{
		totalMinReq += sMin[s];		
	}
	for (var d=1;d<=nDrivers;d++)
	{
		totalMinAvail += dMaxMin[d];
	}
	if (totalMinReq > totalMinAvail)
	{
		writeIn ("not enough driver capacity");
	}	
}

minimize cost;
subject to
{
	cost >=(sum(s in S)sum(b in B)(x_bs[b,s]*bCPKm[b]*sKM[s]+x_bs[b,s]*bCPM[b]*sMin[s]))
	+sum(d in D)((sum(s in S)(x_ds[d,s]*sMin[s])*(1-ed[d])+BM*ed[d])*CBM+(sum(s in S)(x_ds[d,s]*sMin[s])-BM)*CEM*ed[d]);
	sum(d in D)((sum(s in S)(x_ds[d,s]*sMin[s])*(1-ed[d])+BM*ed[d])*CBM+(sum(s in S)(x_ds[d,s]*sMin[s])-BM)*CEM*ed[d]) >= 0;
	//constraint bus capacity
	forall(s in S)
		forall(b in B) bCap[b]>=sLoad[s]*x_bs[b,s];
		
	//constraint max buses
	sum(b in B)x_used[b]<=maxBuses;
	
	forall(b in B)
	  	nServices*x_used[b]>=sum(s in S)x_bs[b,s];
	
	//constraint every service only has one bus  	
	forall(s in S)
	  	sum(b in B)x_bs[b,s]>=1;
	 
	//constraint every service only has one driver
	forall(s in S)
	  	sum(d in D)x_ds[d,s]>=1;
	
	//constraint every service is served
	(sum(b in B)sum(s in S)x_bs[b,s])==nServices;
	(sum(d in D)sum(s in S)x_ds[d,s])==nServices;
	
	//constraint max minutes per driver
	forall(d in D)
	  	sum(s in S)x_ds[d,s]*sMin[s]<=dMaxMin[d];
	  
	//constraint identify extra time per driver
	forall(d in D)
	  	sum(s in S)x_ds[d,s]*sMin[s]-BM<=(dMaxMin[d]-BM+1)*ed[d];
	
	//same bus cannot do services that overlap
	forall(b in B)
	  	forall(s in S)
	  	  forall(s2 in S:sStartTime[s2]<sStartTime[s])
	  	    x_bs[b,s2]*(sStartTime[s2]+sMin[s2])<=sStartTime[s]+1440*(1-x_bs[b,s]);
	//same driver cannot do services that overlap   
	forall(d in D)
	  	forall(s in S)
	  	  forall(s2 in S:sStartTime[s2]<sStartTime[s])
	  	    x_ds[d,s2]*(sStartTime[s2]+sMin[s2])<=sStartTime[s]+1440*(1-x_ds[d,s]);
}




