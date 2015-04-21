// Creates a websocket with socket.io
// Make sure to install socket.io: terminal, goto /var/lib/cloud9 and enter: npm install socket.io
// Installing this takes a few minutes; wait until the installation is complete

// imports
var app = require('http').createServer(handler);
var io = require('/usr/lib/node_modules/bonescript/node_modules/socket.io').listen(app);
var fs = require('fs');
var b = require('bonescript');

// general setup
app.listen(8080);
// socket.io options go here
io.set('log level', 2);   // reduce logging - set 1 for warn, 2 for info, 3 for debug
io.set('browser client minification', true);  // send minified client
io.set('browser client etag', true);  // apply etag caching logic based on version number

console.log('Server running on: http://' + getIPAddress() + ':8080');

// Model namespace
var Model = Model || {};

// water pump
Model.Pump = function (info, tempInfoFrom, tempInfoTo)
{
    var self = this;
    var pumpState = 'Off';
    var overrideState = 'Auto';
    var lastPumpChange = null;
    var fromSensor = new Model.TempSensor(tempInfoFrom);
    var toSensor = new Model.TempSensor(tempInfoTo);

    self.Info = info;

    self.GetOverrideId = function()
    {
        return info.Id + "Override";
    };
    
    self.SetOverride = function (state)
    {
         overrideState = state;
         io.sockets.emit(self.GetOverrideId(), overrideState);
        
        if (state !== 'Auto')
        {
            setPump(state);
            lastPumpChange = null;
        }
    };

    self.DoIt = function()
    {
        // inform clients of state
        io.sockets.emit(info.Id, pumpState);
        io.sockets.emit(self.GetOverrideId(), overrideState);
        
        // read sensors (also informs clients of state)
        var fromTemp = fromSensor.Read();
        var toTemp = toSensor.Read();
        
        if (overrideState === 'Auto')
        {
            doAutoMode(fromTemp, toTemp);
        }
    };

    function doAutoMode(fromTemp, toTemp)
    {
        if (isWithinTimeRange())
        {
            return;
        }

        if (fromTemp > (toTemp + 2))
        {
            setPump('On');
            lastPumpChange = Date.now();
        }
        else if ((toTemp + 2) > fromTemp)
        {
            setPump('Off');
            lastPumpChange = Date.now();
        }
    }

    function isWithinTimeRange()
    {
        if (lastPumpChange === null)
        {
            return false;
        }

        var diff = Date.now() - lastPumpChange;
        
        // change within 1 minute ?
        return diff < 1000 * 60;
    }
    
    function setPump(state)
    {
        console.log(info.Id + ': ' + 'setting state to ' + state);

        pumpState = state;
        b.analogWrite(info.Pin, state === 'On' ? 1 : 0);
        io.sockets.emit(info.Id, state);
    }
    
    function init()
    {
        b.pinMode(info.Pin, b.OUTPUT);
        b.analogWrite(info.Pin, 0);
    }
    
    init();
};

// temperature sensor
Model.TempSensor = function (info)
{
    var TEMP_CNT_FOR_AVG = 10;
    
    var self = this;

    self.Info = info;

    self.tempsRead = new Array();
    self.tempPos = 0;

    self.Read = function()
    {
  //      console.log(info.Id + ': ' + info.Pin);
        self.tempsRead[self.tempPos] = b.analogRead(info.Pin);
        self.tempPos = (self.tempPos + 1) % TEMP_CNT_FOR_AVG;

        var temp = calcTemp(getAvgTemp(self.tempsRead));     
        if(self.tempPos % 2 === 0) {
            io.sockets.emit(info.Id, temp.toFixed(3));
        }
        return temp;
    };

    function getAvgTemp(tempsToAvg)
    {
        var calc = 0;
        
        for (var i=0;i<TEMP_CNT_FOR_AVG;i++)
        { 
            calc += tempsToAvg[i];
        }
        
        return calc/TEMP_CNT_FOR_AVG;
    }
    
    function calcTemp(value)
    {
        var calc = value;
        
        // if sensor has Calc func then call it
        if (info.Calc !== null && info.Calc !== undefined)
        {
            calc = info.Calc(value);
        }
            
        console.log(info.Id + ': ' + value + ' -> ' + calc);
        return calc;
    }
};

// temperature calibration for gable solor temp sensor
function gableSolarTempCalc(sensorReading)
{
    return ((sensorReading / 1.8) * 44);
//    return (((sensorReading * 1.8) * 200) - 273).toFixed(3);
}

// temperature calibration for gable solor temp sensor
function generalTempCalc(sensorReading)
{
    return (((sensorReading * 1.8) * 200) - 273);
//    return (((sensorReading * 1.8) * 200) - 273).toFixed(3);
}

// pumps in the system
var pumps = 
[    
    new Model.Pump(
        { Id:'gableSolarPump', Pin:'P8_19' },
        { Id:'gableSolarTemp', Pin:'P9_37', Calc: gableSolarTempCalc },
        { Id:'mainTankLowerTemp', Pin:'P9_36', Calc: generalTempCalc }
    ),

    new Model.Pump(
        { Id:'backBoilerPump', Pin:'P8_13' },
        { Id:'backBoilerTemp', Pin:'P9_33', Calc: generalTempCalc },
        { Id:'mainTankUpperTemp', Pin:'P9_35', Calc: generalTempCalc}
  
    )
];

// main processing loop
setInterval(runIt, 1000);
function runIt() 
{
    for (var i = 0; i < pumps.length; ++i) 
    {
        pumps[i].DoIt();
    }
}

function handler (req, res) 
{
    if (req.url == "/favicon.ico")
    {   
        // handle requests for favico.ico
        res.writeHead(200, {'Content-Type': 'image/x-icon'} );
        res.end();
        console.log('favicon requested');
        return;
    }
    
     // load html file
    fs.readFile(
        'HotWater.html',
        function (err, data) 
        {
            if (err) 
            {
                res.writeHead(500);
                return res.end('Error loading HotWater.html');
            }
            res.writeHead(200);
            res.end(data);
        });
}

// handles incoming socket messages
io.sockets.on('connection', function (socket) 
{
    socket.on('gableSolarPumpOverride', function (state) 
    {
        setPumpOverride('gableSolarPumpOverride', state);
    });
    socket.on('backBoilerPumpOverride', function (state) 
    {
        setPumpOverride('backBoilerPumpOverride', state);
    });
});

function setPumpOverride(id, state)
{
    for (var i = 0; i < pumps.length; ++i)
    {
        if (pumps[i].GetOverrideId() === id)
        {
            pumps[i].SetOverride(state);
            return;
        }
    }
}

// Get server IP address on LAN
function getIPAddress() 
{
    var interfaces = require('os').networkInterfaces();
    for (var devName in interfaces) 
    {
        var iface = interfaces[devName];
        for (var i = 0; i < iface.length; i++) 
        {
            var alias = iface[i];
            if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal)
                return alias.address;
        }
    }
    
    return '0.0.0.0';
}

 