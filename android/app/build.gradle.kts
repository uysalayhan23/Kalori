import org.gradle.api.tasks.Sync

plugins { id("com.android.application") }

val generatedKaloriWebAssets = layout.buildDirectory.dir("generated/kaloriWebAssets")
val syncKaloriWebAssets by tasks.registering(Sync::class) {
    val webRoot = rootProject.projectDir.parentFile
    from(webRoot) {
        include(
            "index.html", "foods.html", "meal-builder.html", "profile.html",
            "barcode.html", "history.html", "food-catalog.js",
            "packaged-foods.js", "food-quality.js", "journal-data.js", "manifest.webmanifest", "service-worker.js"
        )
    }
    into(generatedKaloriWebAssets)
}

android {
    namespace = "com.kalori.journal"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.kalori.journal"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    sourceSets.getByName("main").assets.srcDir(generatedKaloriWebAssets)
}

// The generated source directory by itself does not reliably schedule the Sync task.
// Merge tasks must wait until the offline HTML/JS assets have actually been copied.
tasks.matching { it.name.startsWith("merge") && it.name.endsWith("Assets") }.configureEach {
    dependsOn(syncKaloriWebAssets)
}
