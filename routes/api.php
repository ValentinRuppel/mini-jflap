<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\OptimizationController;

// ... dentro de tu grupo de rutas protegidas o públicas
Route::post('/optimizar', [OptimizationController::class, 'optimize']);
Route::middleware(['auth:sanctum'])->get('/user', function (Request $request) {
    return $request->user();
});
