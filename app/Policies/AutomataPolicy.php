<?php

namespace App\Policies;

use Illuminate\Auth\Access\Response;
use App\Models\Automata;
use App\Models\User;

class AutomataPolicy
{
    /**
     * Determine whether the user can view any models.
     */
    public function viewAny(User $user): bool
    {
        return false;
    }

    /**
     * Determine whether the user can create models.
     */
    public function create(User $user): bool
    {
        return false;
    }

    public function view(User $user, Automata $automata)
    {
        return $automata->visibility === 'public' || $automata->owner_id === $user->id;
    }

    // Puede editar solo si es el dueño
    public function update(User $user, Automata $automata)
    {
        return $automata->owner_id === $user->id;
    }

    // Puede eliminar solo si es el dueño
    public function delete(User $user, Automata $automata)
    {
        return $automata->owner_id === $user->id;
    }

    /**
     * Determine whether the user can restore the model.
     */
    public function restore(User $user, Automata $automata): bool
    {
        return false;
    }

    /**
     * Determine whether the user can permanently delete the model.
     */
    public function forceDelete(User $user, Automata $automata): bool
    {
        return false;
    }
}
