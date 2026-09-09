package com.example.ui.screens.extensions

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.example.extensions.ExtensionManager

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ExtensionsScreen(onBackClick: () -> Unit) {
    val installedExtensions by ExtensionManager.installedExtensions.collectAsState()
    val availableExtensions = ExtensionManager.availableExtensions

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("الإضافات") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF19191C), titleContentColor = Color.White, navigationIconContentColor = Color.White)
            )
        },
        containerColor = Color(0xFF0F0F11)
    ) { padding ->
        LazyColumn(contentPadding = padding, modifier = Modifier.fillMaxSize()) {
            items(availableExtensions) { ext ->
                val isInstalled = installedExtensions.any { it.id == ext.id }
                ListItem(
                    headlineContent = { Text(ext.name, color = Color.White) },
                    supportingContent = { Text(ext.baseUrl, color = Color.Gray) },
                    trailingContent = {
                        Button(
                            onClick = {
                                if (isInstalled) {
                                    ExtensionManager.uninstallExtension(ext.id)
                                } else {
                                    ExtensionManager.installExtension(ext.id)
                                }
                            },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (isInstalled) Color.DarkGray else Color(0xFFE50914)
                            )
                        ) {
                            Text(if (isInstalled) "إلغاء التثبيت" else "تثبيت", color = Color.White)
                        }
                    },
                    colors = ListItemDefaults.colors(containerColor = Color.Transparent)
                )
                HorizontalDivider(color = Color.DarkGray)
            }
        }
    }
}
