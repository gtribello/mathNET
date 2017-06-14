'use strict'

var myplot = new plotter();

function addGraphFunctionsToApi( interpreter, scope ){
    // Add an API function for updating the graph when there is new data
    var wrapper = function(x,y) {
      x = x ? x.toString() : '';
      y = y ? y.toString() : '';
      return interpreter.createPrimitive(myplot.addDataToGraph(x,y));
    };
    interpreter.setProperty(scope, 'addDataToGraph', interpreter.createNativeFunction(wrapper));
    // Add an API function for drawing the graph based on a table
    var wrapper = function(x,y) {
      x = x ? x.toString() : '';
      y = y ? y.toString() : '';
      return interpreter.createPrimitive(myplot.drawScatterGraphFromTable(x,y));
    };
    interpreter.setProperty(scope, 'drawBarGraphFromTable', interpreter.createNativeFunction(wrapper));
    // Add an API function for drawing the graph based on a table
    var wrapper = function(x,y) {
      x = x ? x.toString() : '';
      y = y ? y.toString() : '';
      return interpreter.createPrimitive(myplot.drawBarGraphFromTable(x,y));
    };
    interpreter.setProperty(scope, 'drawBarGraphFromTable', interpreter.createNativeFunction(wrapper));
    // Add an API function for drawing lines
    var wrapper = function(x1,y1,x2,y2) {
      x1 = x1 ? x1.toString() : '';
      y1 = y1 ? y1.toString() : '';
      x2 = x2 ? x1.toString() : '';
      y2 = y2 ? y1.toString() : '';
      return interpreter.createPrimitive(myplot.drawLine(x1,y1,x2,y2));
    };
    interpreter.setProperty(scope, 'drawLine', interpreter.createNativeFunction(wrapper));
    // Add an API function for adding error lines
    var wrapper = function(e) {
      e = e ? e.toString() : '';
      return interpreter.createPrimitive(myplot.addErrorVal(e));
    };
    interpreter.setProperty(scope, 'addErrorVal', interpreter.createNativeFunction(wrapper));
}

function plotter(){
    this.data = [];
    this.lines = [];
    this.error = [];

    this.options_ = {
      //curveType: 'function',
      width: 400, height: 400,
      chartArea: {left: '10%', width: '85%', height: '85%'}
    };

    this.addErrorVal = function( z ) {
       this.error.push( z );
    }

    this.addDataToGraph = function( x, y ) {
      // Add data to the array containing the data
      this.data.push([x, y]); 
      // And plot the data
      this.plotGraph('graph','scatter');
    };

    this.drawScatterGraphFromTable = function( x, y ) {
      var xnums = x.split(','); var ynums = y.split(',');
      // Check that the lengths of the input vectors are the same
      if( xnums.length!=ynums.length ){ alert("mismatch between number of items in x and y input lists"); return; }
      // Make sure the data table is empty
      this.data.length = 0; this.data.unshift(['x', 'y'], [0, 0]);
      // Add all data to data table 
      for(var i=0; i<xnums.length; i++ ){ this.data.push([xnums[i], ynums[i]]); } 
      // And plot the data
      this.plotGraph('graph','scatter'); 
    };

    this.drawBarGraphFromTable = function( x, y ) {
      var xnums = x.split(','); var ynums = y.split(',');
      // Check that the lengths of the input vectors are the same
      if( xnums.length!=ynums.length ){ alert("mismatch between number of items in x and y input lists"); return; }
      // Make sure the data table is empty
      this.data.length = 0; this.data.unshift(['x', 'y'], [0, 0]);
      // Add all data to data table 
      for(var i=0; i<xnums.length; i++ ){ this.data.push([xnums[i], ynums[i]]); }
      // And plot the data
      this.plotGraph('graph','column');
    };

    this.drawLine = function( x1,y1,x2,y2 ) {
      this.lines.push([x1-0,y1-0,x2-0,y2-0]);
    };

    this.plotGraph = function(div_id,gtype) {
      if( this.error.length>0 ){
          var data = new google.visualization.DataTable();
          data.addColumn('number', this.data[0] );
          data.addColumn('number', this.data[1] );
          data.addColumn({type: 'number', id: "errtop", role: 'interval'});
          data.addColumn({type: 'number', id: "errbot", role: 'interval'}); 
          for(var i=1;i<this.data.length;i++){
              var y = this.data[i][1]-0; var err = this.error[i-1]-0;
              data.addRow([this.data[i][0]-0,y,y+err,y-err]);
          }
          new google.visualization.ScatterChart(document.getElementById(div_id)).draw(data,{
             width: 400, height: 400,
             chartArea: {left: '10%', width: '85%', height: '85%'},
             intervals: { style: 'bars' }   
          });
      } else if( this.lines.length>0 ){
          var data = new google.visualization.DataTable();
          data.addColumn('number', this.data[0] );
          data.addColumn('number', this.data[1] );
          var firstrow = []; firstrow.push(0); firstrow.push(null);
          for(var i=0;i<this.lines.length;i++){ 
              data.addColumn('number','line' + i ); 
              firstrow.push(this.lines[i][1]);
          } 
          data.addRow(firstrow);
          for(var i=1;i<this.data.length;i++){ 
              var row = []; row.push(this.data[i][0]-0); row.push(this.data[i][1]-0);
              for(var j=0;j<this.lines.length;j++){ row.push(null); }
              data.addRow(row); 
          }
          var lastrow = []; lastrow.push(10); lastrow.push(null);
          for(var i=0;i<this.lines.length;i++){ lastrow.push(this.lines[i][1]); }
          data.addRow(lastrow);
          new google.visualization.ComboChart(document.getElementById(div_id)).draw(data,{
             width: 400, height: 400,
             chartArea: {left: '10%', width: '85%', height: '85%'},
             interpolateNulls: true,
             series: {
                0: { pointShape: 'circle', type: 'scatter' },
                1: { type: 'line' },
                2: { type: 'line' }
             } 
          });
      } else {
          // Create the data table from the stored data.
          var data = google.visualization.arrayToDataTable(this.data);
          // Create and draw the visualization, passing in the data and options.
          if( gtype=='scatter' ){
             new google.visualization.ScatterChart(document.getElementById(div_id)).draw(data, this.options_);
          } else if( gtype=='column' ){
             new google.visualization.ColumnChart(document.getElementById(div_id)).draw(data, this.options_);
          } else if( gtype=='line' ){
             new google.visualization.LineChart(document.getElementById(div_id)).draw(data, this.options_);
          }
      }
    };
}

// Define a custom block to add data to the graph
Blockly.Blocks["draw_error_bar"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "plot point at x = %1 and %2 with y-error bar %3",
      "args0": [
        {
          "type": "input_value",
          "name": "X"
        },
        {
         "type": "input_value",
         "name": "Y"
        },
        {
         "type": "input_value",
         "name": "Z"
        }
      ],
      "inputsInline": true,
      "nextStatement": null,
      "previousStatement": null,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    });
  }
};

Blockly.JavaScript['draw_error_bar'] = function(block) {
  var x = Blockly.JavaScript.valueToCode(block, 'X', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var y = Blockly.JavaScript.valueToCode(block, 'Y', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var z = Blockly.JavaScript.valueToCode(block, 'Z', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'addErrorVal(' + z + ');\naddDataToGraph(' + x + ', ' + y + ');\n';
  return code;
};

Blockly.Python['draw_error_bar'] = function(block) {
  var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
  var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
  var z = Blockly.Python.valueToCode(block, 'Z', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'addDataWithErrorToGraph(' + x + ', ' + y + ',' + z + ')\n';
  return code;
};

// Define a custom block to add data to the graph
Blockly.Blocks["draw_point"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "plot point at x = %1",
      "args0": [
        {
          "type": "input_value",     
          "name": "X"
        }
      ],
      "message1": " and y = %1",
      "args1": [
        {
         "type": "input_value",     
         "name": "Y"
        }
      ],
      "inputsInline": true,
      "nextStatement": null,
      "previousStatement": null,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    });
  } 
};

Blockly.JavaScript['draw_point'] = function(block) {
  var x = Blockly.JavaScript.valueToCode(block, 'X', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var y = Blockly.JavaScript.valueToCode(block, 'Y', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'addDataToGraph(' + x + ', ' + y + ');\n';
  return code; 
};

Blockly.Python['draw_point'] = function(block) {
  var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
  var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'addDataToGraph(' + x + ', ' + y + ')\n';
  return code;
};

// Define a custom block to draw a graph based on a table
Blockly.Blocks["draw_list"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "plot table with x = %1",
      "args0": [
        {
          "type": "input_value",
          "name": "X",
          "check": "Array"
        }
      ],
      "message1": " and y = %1",
      "args1": [
        {
         "type": "input_value",
         "name": "Y",
         "check": "Array"
        }
      ],
      "inputsInline": true,
      "nextStatement": null,
      "previousStatement": null,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    });
  }
};

Blockly.JavaScript['draw_list'] = function(block) {
  var x = Blockly.JavaScript.valueToCode(block, 'X', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var y = Blockly.JavaScript.valueToCode(block, 'Y', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'drawScatterGraphFromTable(' + x + ', ' + y + ');\n';
  return code;
};

Blockly.Python['draw_list'] = function(block) {
  var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
  var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'matplotlib.pyplot.plot(' + x + ', ' + y + ')\nmatplotlib.pyplot.show()';
  return code;
};

// Define a custom block to draw a bar chart based on a table
Blockly.Blocks["draw_bar_chart"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "plot bar chart with x = %1",
      "args0": [
        {
          "type": "input_value",
          "name": "X",
          "check": "Array"
        }
      ],
      "message1": " and y = %1",
      "args1": [
        {
         "type": "input_value",
         "name": "Y",
         "check": "Array"
        }
      ],
      "inputsInline": true,
      "nextStatement": null,
      "previousStatement": null,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    });
  }
};

Blockly.JavaScript['draw_bar_chart'] = function(block) {
  var x = Blockly.JavaScript.valueToCode(block, 'X', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var y = Blockly.JavaScript.valueToCode(block, 'Y', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'drawBarGraphFromTable(' + x + ', ' + y + ');\n';
  return code;
};

Blockly.Python['draw_bar_chart'] = function(block) {
  var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
  var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'matplotlib.pyplot.bar(' + x + ', ' + y + ', 0.4 )\nmatplotlib.pyplot.show()';
  return code;
};

// Define a custom block to draw a horizontal or vertical line
Blockly.Blocks["draw_line"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "draw %1 line at %2",
      "args0": [
         {
           "type": "field_dropdown",
           "name": "OP",
           "options": [
             ['horizontal', 'HORIZONTAL'],
             ['vertical', 'VERTICAL']
           ]
         },
         {
           "type": "input_value",
           "name": "NUM",
           "check": "Number"
         }
      ],
      "inputsInline": true,
      "nextStatement": null,
      "previousStatement": null,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    });  
  }      
};

Blockly.JavaScript['draw_line'] = function(block) {
  var code; var ftype = block.getFieldValue('OP');
  var x = Blockly.JavaScript.valueToCode(block, 'NUM', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  switch(ftype){ 
  case("HORIZONTAL") :
     var x1=0; var x2=10; code = 'drawLine(' + x1 + ','  + x  + ',' + x2 + ',' + x + ')\n'; break; 
  case("VERTICAL") : 
     var y1=0; var y2=1; code = 'drawLine(' + x + ',' + y1 + ',' + x + ',' + y2 + ')\n'; break; 
  } 
  return code; 
}; 

Blockly.Python['draw_line'] = function(block) {
  var code; var ftype = block.getFieldValue('OP');
  var x = Blockly.Python.valueToCode(block, 'NUM', Blockly.Python.ORDER_ATOMIC) || '0';
  switch(ftype){ 
  case("HORIZONTAL") : 
     code = 'matplotlib.pyplot.plot( [0,10],[' +  x  + ',' + x + '], k- )\n'; break; 
  case("VERTICAL") : 
     code = 'matplotlib.pyplot.plot([' + x + ',' + x + '], [0,1], k- )\n'; break; 
  } 
  return code;
};
