'use strict'
    
var random = new randomVariablesClass();
      
function addRandomVariablesApi( interpreter, scope ){
   // Add an API function for normal random variables
   var wrapper = function(id) {
     id = id ? id.toString() : '';
     return interpreter.createPrimitive(random.normalRandom(id));
   };
   interpreter.setProperty(scope, 'normalRandom', interpreter.createNativeFunction(wrapper));
   // Add an API function for cumulative probability distribution function
   var wrapper = function(id) {
     id = id ? id.toString() : '';
     return interpreter.createPrimitive(myApp.erf(id));
   };
   interpreter.setProperty(scope, 'erf', interpreter.createNativeFunction(wrapper));

   // Add an API function for inverse cumulative probability distribution function
   var wrapper = function(id) {
     id = id ? id.toString() : '';
     return interpreter.createPrimitive(myApp.NormSInv(id));
   };
   interpreter.setProperty(scope, 'NormSInv', interpreter.createNativeFunction(wrapper));
}

function randomVariablesClass(){
   // This generates normal random variables
   this.normalRandom = function() {
      var V1, V2, S;
       do {
         var U1 = Math.random();
         var U2 = Math.random();
         V1 = 2 * U1 - 1;
         V2 = 2 * U2 - 1;
         S = V1 * V1 + V2 * V2;
       } while (S > 1);
       return Math.sqrt(-2 * Math.log(S) / S) * V1;
   };
}

// Define a custom block to generate uniform random variables
Blockly.Blocks["uniform_random"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "uniform random variable between 0 and 1",
      "output": "Number",
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    })
  }
};

Blockly.JavaScript['uniform_random'] = function(block) {
  var code = 'Math.random()'; 
  return [code, Blockly.JavaScript.ORDER_ATOMIC]; 
};

Blockly.Python['uniform_random'] = function(block) {
  var code = 'numpy.random.uniform(0,1)'; 
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Define a custom block to generate normal random variables
Blockly.Blocks["normal_random"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "standard normal random variable",
      "output": "Number",
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    })
  }
};

Blockly.JavaScript['normal_random'] = function(block) {
  var code = 'normalRandom()'; 
  return [code, Blockly.JavaScript.ORDER_ATOMIC]; 
};

Blockly.Python['normal_random'] = function(block) {
  var code = 'numpy.random.normal()'; 
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Define a custom block to do the mathematics of the standard normal distribution
Blockly.Blocks["math_normal"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "%1 of cumulative distribution for standard normal random variable at %2",
      "args0": [
         {
           "type": "field_dropdown",
           "name": "OP",
           "options":
             [['value', 'VALUE'],
             ['value of inverse', 'INVERSE']]
         },
         {
           "type": "input_value",
           "name": "NUM",
           "check": "Number"
         }
      ],
      "output": "Number",
      "inputsInline": true,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP
    })
  }
};

Blockly.JavaScript['math_normal'] = function(block) {
  var code; var ftype = block.getFieldValue('OP');
  var x = Blockly.JavaScript.valueToCode(block, 'NUM', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  switch(ftype){
  case("VALUE") :
     code = 'erf(' + x  + ')'; break;
  case("INVERSE") :
     code = 'NormSInv(' + x + ')'; break;
  }
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.Python['math_normal'] = function(block) {
  var code; var ftype = block.getFieldValue('OP');
  var x = Blockly.Python.valueToCode(block, 'NUM', Blockly.Python.ORDER_ATOMIC) || '0';
  switch(ftype){
  case("VALUE") :
     code = 'scipi.stats.norm.cdf(' + x + ')'; break;
  case("INVERSE") :
     code = 'scipi.stats.norm.ppf(' + x + ')'; break;
  }
  return [code, Blockly.Python.ORDER_ATOMIC];
};
