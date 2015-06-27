
'use strict';

var app = angular.module('HotWater', []);

// configure angular to avoid brace conflicts with Jinja2
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
});

app.controller('TempSensorsController', ['$scope', '$http', '$log', TempSensorsController]);

app.overrideSwitch = function (selector) {
  $.getJSON("/Gable/" + selector.value, function (data) { })
}

function TempSensorsController($scope, $http, $log) {

  $scope.get_tempsensors = function() {
    $http.get('/tempsensors')
      .success(function(data) { $scope.tempsensors = data.tempsensors; })
      .error(function(data) { $log.log('eek!'); });
  }

  $scope.get_tempsensors();
}
