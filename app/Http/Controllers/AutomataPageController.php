<?php

namespace App\Http\Controllers;

use Inertia\Inertia;

class AutomataPageController extends Controller
{
    public function index()
    {
        return Inertia::render('Automatas/Index');
    }
}
    
