<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Automata;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests; 
use Illuminate\Foundation\Validation\ValidatesRequests;

class AutomataShareController extends Controller
{
    use AuthorizesRequests, ValidatesRequests;
    public function store(Request $request, Automata $automata)
    {
        $this->authorize('update', $automata); // solo el dueño puede compartir

        $data = $request->validate([
            'email' => 'required|email',
            'permiso' => 'required|in:view,edit',
        ]);

        $user = User::where('email', $data['email'])->first();

        if (!$user) {
            return response()->json(['error' => 'Usuario no encontrado'], 404);
        }

        $automata->compartidosCon()->syncWithoutDetaching([
            $user->id => ['permiso' => $data['permiso']]
        ]);

        return response()->json(['message' => 'Autómata compartido con éxito']);
    }

    public function index(Automata $automata)
    {
        $this->authorize('view', $automata);

        $shares = $automata->compartidosCon()->get(['users.id', 'users.email', 'automata_shares.permiso']);
        return response()->json($shares);
    }

    public function destroy(Automata $automata, $userId)
    {
        $this->authorize('update', $automata);
        $automata->compartidosCon()->detach($userId);

        return response()->json(['message' => 'Acceso eliminado']);
    }
}

