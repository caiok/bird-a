'use strict';

/**
 * @ngdoc overview
 * @name birdaApp
 * @description
 * # birdaApp
 *
 * Main module of the application.
 */

/*
 * Constants declaration
 */
const RDF_TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type';


/*
 * Angular initialization
 */
angular
	.module('birdaApp', [
		'ngAnimate',
		'ngCookies',
		'ngResource',
		'ngRoute',
		'ngSanitize',
		'ngTouch',
		'ui.bootstrap'
	])
	.config(function ($routeProvider, $locationProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'views/home.html',
			})
			.when('/contact', {
				templateUrl: 'views/contact.html',
			})
			.when('/forms-list', {
				templateUrl: 'views/forms-list.html',
				//controller: 'FormsListController',
				//controllerAs: 'cFormsList',
			})
			.when('/individuals-list', {
				templateUrl: 'views/individuals-list.html',
			})
			.when('/contact', {
				templateUrl: 'views/contact.html',
			})

			.when('/404', {
				templateUrl: 'views/404.html',
			})
			.otherwise({
				redirectTo: '/404',
			});

		$locationProvider.html5Mode({
			enabled: true,
			requireBase: false
		});
	});
