// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;
use std::process::Command;
use std::sync::Mutex;

struct BackendProcess(Mutex<Option<std::process::Child>>);

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(BackendProcess(Mutex::new(None)))
        .setup(|app| {
            let handle = app.app_handle().clone();
            std::thread::spawn(move || {
                let child = Command::new("python")
                    .args(["-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8001"])
                    .current_dir("../backend")
                    .spawn();

                match child {
                    Ok(proc) => {
                        println!("Backend started successfully on port 8001.");
                        if let Some(state) = handle.try_state::<BackendProcess>() {
                            if let Ok(mut lock) = state.0.lock() {
                                *lock = Some(proc);
                            }
                        }
                    }
                    Err(e) => {
                        eprintln!("Failed to start backend: {}", e);
                    }
                }
            });
            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                if let Some(state) = window.try_state::<BackendProcess>() {
                    if let Ok(mut lock) = state.0.lock() {
                        if let Some(mut child) = lock.take() {
                            let _ = child.kill();
                            let _ = child.wait();
                            println!("Backend process terminated cleanly.");
                        }
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
