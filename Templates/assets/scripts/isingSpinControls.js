'use strict'

var ising = new isingSpinControls();

function addIsingFunctionsToApi( interpreter, scope ){
    // Add API functions for number of spins
    var wrapper = function(){
      return interpreter.createPrimitive(ising.getNumberOfSpins());
    };
    interpreter.setProperty(scope, 'getNumberOfSpins', interpreter.createNativeFunction(wrapper));

    // Add API functions for magnetic field strength
    var wrapper = function(){
      return interpreter.createPrimitive(ising.getMagneticField());
    };
    interpreter.setProperty(scope, 'getMagneticField', interpreter.createNativeFunction(wrapper));

    // Add API functions for temperature
    var wrapper = function(){
      return interpreter.createPrimitive(ising.getTemperature());
    };
    interpreter.setProperty(scope, 'getTemperature', interpreter.createNativeFunction(wrapper));

    // Add API function for setting spins
    var wrapper = function(ida, idb){
      ida = ida ? ida.toString() : '';
      idb = idb ? idb.toString() : '';
      return interpreter.createPrimitive(ising.setSpinValue(ida,idb));
    };
    interpreter.setProperty(scope, 'setSpinValue', interpreter.createNativeFunction(wrapper));

    // Add API function for getting spins
    var wrapper = function(id){
      id = id ? id.toString() : '';
      return interpreter.createPrimitive(ising.getSpinValue(id));
    };
    interpreter.setProperty(scope, 'getSpinValue', interpreter.createNativeFunction(wrapper))
}

function isingSpinControls(){
    this.potts = false;
    this.spins = []; this.nspins = 25;
    this.magneticFieldStrength = 0.;
    this.temperature = 1.;
    this.radius = 200;

    this.drawSpin = function( snum ){
      var ctx = document.getElementById("myCanvas").getContext("2d");
      if ( ctx==null ){ return; }
      var num = parseInt( snum );

      ctx.beginPath(); var unit = 2*Math.PI/this.spins.length; var radius=this.radius; var infr=0.9;
      ctx.moveTo(radius+radius*Math.cos((num+1)*unit),radius+radius*Math.sin((num+1)*unit));
      ctx.lineTo(radius+infr*radius*Math.cos((num+1)*unit),radius+infr*radius*Math.sin((num+1)*unit));
      ctx.lineTo(radius+infr*radius*Math.cos(num*unit),radius+infr*radius*Math.sin(num*unit));
      ctx.lineTo(radius+radius*Math.cos(num*unit),radius+radius*Math.sin(num*unit));
      ctx.closePath();

      if( this.spins[num]==0 ){
         ctx.stroke();
         return;
      }
      if( this.potts ) {
         if (this.spins[num] == 0 ) {
            ctx.fillStyle = '#8ED6FF';
         } else if( this.spins[num] == 1 ) {
            ctx.fillStyle = '#FF0000';
         } else if( this.spins[num] == 2 ) {
            ctx.fillStyle = '#33FF36';
         } else {
            ctx.fillStyle = '#FF33CE';
         }
      } else {
         if (this.spins[num] == 1 ) {
            ctx.fillStyle = '#8ED6FF';
         } else {
            ctx.fillStyle = '#FF0000';
         }
      }
      ctx.stroke();
      ctx.fill();
   };

   this.getAverageSpin = function() {
      var tspin = 0.;
      for(var i=0 ; i < this.spins.length ; i++ ){ 
          tspin += this.spins[i];
      }
      return tspin / this.spins.length;
   };

   this.hamiltonian=function( meanfield ){
      if( meanfield ){
          var aspin = this.getAverageSpin(); var eng = 0.;
          for(var i=0 ; i < this.spins.length ; i++ ){
              eng += -( 2*aspin + this.magneticFieldStrength )*this.spins[i];
          }
          return eng;
      } 
      var eng = 0.; eng += -this.spins[0]*this.spins[this.spins.length-1] - this.spins[0]*this.magneticFieldStrength;
      for(var i = 1; i < this.spins.length; i++){
          eng += -this.spins[i-1]*this.spins[i] - this.magneticFieldStrength*this.spins[i];
      } 
      return eng;
   };

   this.getSpinValue=function( n ) {
     if( n>=this.spins.length || n < 0 ){
         alert( "spin " + n + " does not exist" );
     }
     if( this.spins[n]!=1 && this.spins[n]!=-1 ){
         alert( "spin " + n + " has illegal value");
     }
     return this.spins[n];
   };

   this.setSpinValue=function( n, val ) {
     if( n>=this.spins.length || n < 0 ){
         alert( "spin " + n + " does not exist" );
     }
     if( !this.potts & val!=1 && val!=-1 ){
         alert( val + " is not a valid spin value" );
     } else if( this.potts && val!=0 && val!=1 && val!=2 && val!=3 ) {
         alert( val + " is not a valid spin value" );
     }
     this.spins[n] = parseInt( val );
     this.drawSpin( n );
   };

   this.setNumberOfSpins=function( nspins ) {
      this.nspins=nspins; this.spins = [];
      var ctx = document.getElementById("myCanvas").getContext("2d");
      if( ctx!=null ){ ctx.clearRect(0,0,400,400); }
      for(var i = 0; i < nspins; i++){ this.spins.push( 0 ); }
      for(var i = 0; i < nspins; i++){ this.drawSpin( i ); }
   };

   this.getNumberOfSpins=function() {
     return this.spins.length;
   };

   this.setMagneticField=function(val) {
     this.magneticFieldStrength = val;
   };

   this.getMagneticField=function() {
     return this.magneticFieldStrength;
   };

   this.setTemperature=function(val) {
     this.temperature = val;
   };

   this.getTemperature=function() {
     return this.temperature;
   };
}

// Return the magnetic field strength
Blockly.Blocks["get_field"] = {
  init: function() {
    this.jsonInit({
      "message0": "get magnetic field strength",
      "output": "Number",
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    })
  }
};

Blockly.JavaScript['get_field'] = function(block) {
  var code = 'getMagneticField()';
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.Python['get_field'] = function(block) {
  var code = 'magnetic_field_strength';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Return the temperature
Blockly.Blocks["get_temperature"] = {
  init: function() {
    this.jsonInit({
      "message0": "get temperature",
      "output": "Number",
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    })
  }
};

Blockly.JavaScript['get_temperature'] = function(block) {
  var code = 'getTemperature()';
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.Python['get_temperature'] = function(block) {
  var code = 'temperature';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Return the number of spins in the system
Blockly.Blocks["get_nspins"] = {
  init: function() {
    this.jsonInit({
      "message0": "number of spins",
      "output": "Number",
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    })
  }
};

Blockly.JavaScript['get_nspins'] = function(block) {
  var code = 'getNumberOfSpins()';
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.Python['get_nspins'] = function(block) {
  var code = 'nspins';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Get the value of the ith spin
Blockly.Blocks["get_spin"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "get spin %1",
      "args0": [
        {
          "type": "input_value",
          "name": "n",
          "check": "Number"
        }
      ],
      "output": "Number",
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    })
  }
};

Blockly.JavaScript['get_spin'] = function(block) {
  var s = Blockly.JavaScript.valueToCode(block, 'n', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'getSpinValue(' + s  + ')';
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.Python['get_spin'] = function(block) {
  var s = Blockly.Python.valueToCode(block, 'n', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'spins[' + s  + ']';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks["set_spin"] = {
  init: function() {
    this.jsonInit({
      "message0": "set spin %1",
      "args0": [
        {
          "type": "input_value",
          "name": "n",
          "check": "Number"
        }
      ],
      "message1": " to %1",
      "args1": [
        {
          "type": "input_value",
          "name": "v",
          "check": "Number"
        }
      ],
      "inputsInline": true,
      "nextStatement": null,
      "previousStatement": null,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    })
  }
};

Blockly.JavaScript['set_spin'] = function(block) {
  var s = Blockly.JavaScript.valueToCode(block, 'n', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var v = Blockly.JavaScript.valueToCode(block, 'v', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'setSpinValue(' + s + ',' + v + ');\n';
  return code;
};

Blockly.Python['set_spin'] = function(block) {
  var s = Blockly.Python.valueToCode(block, 'n', Blockly.Python.ORDER_ATOMIC) || '0';
  var v = Blockly.Python.valueToCode(block, 'v', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'spins[' + s + '] = ' + v + '\n';
  return code;
};


