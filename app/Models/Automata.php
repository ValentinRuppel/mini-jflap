<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Automata extends Model
{
    protected $fillable = ['nombre', 'tipo', 'json_definicion'];

    protected $casts = [
        'json_definicion' => 'array',
    ];
}

