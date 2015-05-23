
"use strict";

// namespace
var HotWater = HotWater || {};

var app;
$(document).ready(function ()
{
    app = new HotWater.App();
});

HotWater.App = function ()
{
    var self = this;

    self.overrideSwitch = function (selector)
    {
        $.getJSON("/Gable/" + selector.value, function(data) { })
    }
}

