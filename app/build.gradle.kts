plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "local.opd2515.antirootdialogblocker"
    compileSdk = 35

    defaultConfig {
        applicationId = "local.opd2515.antirootdialogblocker"
        minSdk = 29
        targetSdk = 35
        versionCode = 2
        versionName = "1.1"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles("proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    packaging {
        resources {
            merges += "META-INF/xposed/*"
        }
    }

    lint {
        abortOnError = true
        checkReleaseBuilds = true
    }
}

dependencies {
    compileOnly(libs.libxposed.api)
}
