<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AutomataController;

Route::get('/', function () {
    return view('welcome');
});

Route::prefix('api')->group(function () {
    Route::apiResource('automatas', AutomataController::class);
    Route::post('automatas/{automata}/probar', [AutomataController::class, 'probar']);
});


