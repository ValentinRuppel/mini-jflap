<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use App\Http\Controllers\AutomataPageController;
use Illuminate\Support\Facades\Auth;
Route::get('/', function () {
    if (Auth::check()) {
        return redirect()->route('automatas.index'); 
    }
    return Inertia::render('Welcome', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
});


Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('/automatas', [AutomataPageController::class, 'index'])->name('automatas.index');
    Route::get('/automatas/create', [AutomataPageController::class, 'create'])->name('automatas.create');
    Route::post('/automatas', [AutomataPageController::class, 'store'])->name('automatas.store');
    Route::get('/automatas/{automata}', [AutomataPageController::class, 'show'])->name('automatas.show');
    Route::get('/automatas/{automata}/edit', [AutomataPageController::class, 'edit'])->name('automatas.edit');
    Route::put('/automatas/{automata}', [AutomataPageController::class, 'update'])->name('automatas.update');
    Route::delete('/automatas/{automata}', [AutomataPageController::class, 'destroy'])->name('automatas.destroy');
    Route::post('/automatas/{automata}/optimizar', [AutomataPageController::class, 'optimize'])->name('automatas.optimize');
});

require __DIR__.'/auth.php';
