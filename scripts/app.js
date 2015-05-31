
'use strict';

var app = angular.module('HotWater', []);

// configure angular to avoid brace conflicts with Jinja2
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
});

app.controller('ThermostatsController', ['$scope', '$http', '$log', ThermostatsController]);

app.overrideSwitch = function (selector) {
  $.getJSON("/Gable/" + selector.value, function (data) { })
}

function ThermostatsController($scope, $http, $log) {
  $http.get('/thermostats')
    .success(function(data) { $scope.thermostats = data.thermostats; })
    .error(function(data) { $log.log('eek!'); });
}
