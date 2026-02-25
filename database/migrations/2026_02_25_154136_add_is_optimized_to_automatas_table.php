<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up()
    {
        Schema::table('automatas', function (Blueprint $table) {
            $table->boolean('is_optimized')->default(false)->after('json_definicion');
        });
    }

    public function down()
    {
        Schema::table('automatas', function (Blueprint $table) {
            $table->dropColumn('is_optimized');
        });
    }
};
