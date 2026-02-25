<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\User;

class Automata extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'nombre',
        'tipo',
        'json_definicion',
        'is_optimized',
    ];

    protected $casts = [
        'json_definicion' => 'array',
    ];

    // Relación con el usuario propietario
    public function user()
    {
        return $this->belongsTo(User::class);
    }
    public function compartidosCon()
    {
        return $this->belongsToMany(User::class, 'automata_shares')
                    ->withPivot('permiso')
                    ->withTimestamps();
    }

}

