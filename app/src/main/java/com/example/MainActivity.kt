package com.example

import android.Manifest
import android.os.Build
import com.example.extensions.ExtensionManager
import com.example.extensions.providers.WitAnimeExtension
import com.example.extensions.providers.LegacySiteExtension
import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.core.app.ActivityCompat
import androidx.core.os.LocaleListCompat
import com.example.data.repository.UserPreferencesRepository
import com.example.navigation.AppNavigation
import com.example.ui.theme.MyApplicationTheme
import com.example.utils.NotificationHelper
import com.startapp.sdk.adsbase.StartAppAd
import com.startapp.sdk.adsbase.StartAppSDK

class MainActivity : AppCompatActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    
    super.onCreate(savedInstanceState)
    
    ExtensionManager.init(this)
    ExtensionManager.registerExtension(WitAnimeExtension())

    val legacyAnime = listOf("w1.anime4up.rest", "animeblkom.net", "animeat.net", "arabanime.net", "det.animerco.org", "vip.animeluxe.org")
    val legacyMovies = listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", "topcinema.io", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", "stardima.com", "watch.stardima.com", "uo.brstej.com", "laaroza.space")
    
    legacyAnime.forEach { name ->
        ExtensionManager.registerExtension(LegacySiteExtension(name, name, "https://$name", true, false, false))
    }
    legacyMovies.forEach { name ->
        ExtensionManager.registerExtension(LegacySiteExtension(name, name, "https://$name", false, true, true))
    }


    
    // Initialize Start.io SDK with a placeholder App ID.
    // Replace "208324071" with your actual Start.io App ID.
    StartAppSDK.init(this, "208324071", false)
    StartAppAd.disableSplash()
    
    NotificationHelper.createChannel(this)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.POST_NOTIFICATIONS), 101)
    }
    enableEdgeToEdge()
    
    val userPreferences = UserPreferencesRepository(this)
    
    setContent {
      val themeMode by userPreferences.themeMode.collectAsState(initial = 0)
      val primaryColor by userPreferences.primaryColor.collectAsState(initial = 0)
      val appLanguage by userPreferences.appLanguage.collectAsState(initial = null)
      
      // Update app language
      LaunchedEffect(appLanguage) {
          if (appLanguage != null) {
              val currentLocales = AppCompatDelegate.getApplicationLocales()
              val desiredLanguage = if (appLanguage == "system") "" else appLanguage!!
              
              val currentTag = if (currentLocales.isEmpty) "" else currentLocales.toLanguageTags()
              
              val needsUpdate = if (desiredLanguage.isEmpty()) {
                  !currentLocales.isEmpty
              } else {
                  !currentTag.startsWith(desiredLanguage)
              }
              
              if (needsUpdate) {
                  if (desiredLanguage.isEmpty()) {
                      AppCompatDelegate.setApplicationLocales(LocaleListCompat.getEmptyLocaleList())
                  } else {
                      AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(desiredLanguage))
                  }
              }
          }
      }

      MyApplicationTheme(
          themeMode = themeMode,
          primaryColor = primaryColor
      ) {
        Surface(modifier = Modifier.fillMaxSize()) {
          AppNavigation()
        }
      }
    }
  }
}
