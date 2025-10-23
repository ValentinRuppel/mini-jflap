<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\User;

class Automata extends Model
{
    use HasFactory;

    protected $fillable = [
        'nombre',
        'tipo',
        'json_definicion',
        'owner_id',
        'visibility',
    ];

    protected $casts = [
        'json_definicion' => 'array',
    ];

    // Relación con el usuario propietario
    public function owner()
    {
        return $this->belongsTo(User::class, 'owner_id');
    }
    public function compartidosCon()
    {
        return $this->belongsToMany(User::class, 'automata_shares')
                    ->withPivot('permiso')
                    ->withTimestamps();
    }

}

