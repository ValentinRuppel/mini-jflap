<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class AutomataShare extends Model
{
    protected $fillable = ['automata_id', 'user_id', 'permiso'];

    public function automata()
    {
        return $this->belongsTo(Automata::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}

