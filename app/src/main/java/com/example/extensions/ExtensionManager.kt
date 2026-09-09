package com.example.extensions

import android.content.Context
import android.content.SharedPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

object ExtensionManager {
    private const val PREFS_NAME = "extensions_prefs"
    private const val INSTALLED_KEY = "installed_extensions"

    private lateinit var prefs: SharedPreferences
    
    // Store all available extensions
    private val _availableExtensions = mutableListOf<ProviderExtension>()
    val availableExtensions: List<ProviderExtension> get() = _availableExtensions

    // Reactive state for installed extensions
    private val _installedExtensions = MutableStateFlow<List<ProviderExtension>>(emptyList())
    val installedExtensions: StateFlow<List<ProviderExtension>> = _installedExtensions.asStateFlow()

    fun init(context: Context) {
        prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        loadInstalled()
    }

    fun registerExtension(extension: ProviderExtension) {
        if (_availableExtensions.none { it.id == extension.id }) {
            _availableExtensions.add(extension)
        }
    }

    private fun loadInstalled() {
        val installedIds = prefs.getStringSet(INSTALLED_KEY, emptySet()) ?: emptySet()
        val installed = _availableExtensions.filter { it.id in installedIds }
        _installedExtensions.value = installed
    }

    fun installExtension(extensionId: String) {
        val currentIds = prefs.getStringSet(INSTALLED_KEY, emptySet())?.toMutableSet() ?: mutableSetOf()
        currentIds.add(extensionId)
        prefs.edit().putStringSet(INSTALLED_KEY, currentIds).apply()
        loadInstalled()
    }

    fun uninstallExtension(extensionId: String) {
        val currentIds = prefs.getStringSet(INSTALLED_KEY, emptySet())?.toMutableSet() ?: mutableSetOf()
        currentIds.remove(extensionId)
        prefs.edit().putStringSet(INSTALLED_KEY, currentIds).apply()
        loadInstalled()
    }

    fun isInstalled(extensionId: String): Boolean {
        val currentIds = prefs.getStringSet(INSTALLED_KEY, emptySet()) ?: emptySet()
        return currentIds.contains(extensionId)
    }
}
