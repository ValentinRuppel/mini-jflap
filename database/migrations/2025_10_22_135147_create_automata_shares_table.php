<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('automata_shares', function (Blueprint $table) {
            $table->id();
            $table->foreignId('automata_id')->constrained('automatas')->cascadeOnDelete();
            $table->foreignId('user_id')->constrained('users')->cascadeOnDelete();
            $table->enum('permiso', ['view', 'edit'])->default('view');
            $table->timestamps();

            $table->unique(['automata_id', 'user_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('automata_shares');
    }
};

