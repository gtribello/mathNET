'use strict'
    
var random = new randomVariablesClass();
      
function addRandomVariablesApi( interpreter, scope ){
   // Add an API function for normal random variables
   var wrapper = function(id) {
     id = id ? id.toString() : '';
     return interpreter.createPrimitive(random.normalRandom(id));
   };
   interpreter.setProperty(scope, 'normalRandom', interpreter.createNativeFunction(wrapper));
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
