// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::fs::File;
use std::path::Path;

struct BackendProcess(Mutex<Option<Child>>);

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(BackendProcess(Mutex::new(None)))
        .setup(|app| {
            let handle = app.app_handle().clone();
            std::thread::spawn(move || {
                let backend_src_dir = if Path::new("D:/GURUKUL/backend/src").exists() {
                    "D:/GURUKUL/backend/src"
                } else if Path::new("../backend/src").exists() {
                    "../backend/src"
                } else if Path::new("backend/src").exists() {
                    "backend/src"
                } else if Path::new("../../backend/src").exists() {
                    "../../backend/src"
                } else {
                    "../backend/src"
                };

                let log_dir = Path::new("D:/GURUKUL/backend/logs");
                let _ = std::fs::create_dir_all(&log_dir);
                let log_file = File::create(log_dir.join("backend_spawn.log")).unwrap_or_else(|_| File::create("backend_spawn.log").unwrap());

                let python_cmds = vec![
                    vec!["/c", "python", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"],
                    vec!["/c", "py", "-3", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"],
                    vec!["/c", "python3", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"]
                ];

                let mut spawned_child = None;
                for args in python_cmds {
                    let child_res = Command::new("cmd")
                        .args(&args)
                        .current_dir(backend_src_dir)
                        .stdout(Stdio::from(log_file.try_clone().unwrap()))
                        .stderr(Stdio::from(log_file.try_clone().unwrap()))
                        .spawn();

                    match child_res {
                        Ok(proc) => {
                            println!("Backend started successfully using cmd {:?} in directory '{}' on port 8001.", args, backend_src_dir);
                            spawned_child = Some(proc);
                            break;
                        }
                        Err(e) => {
                            eprintln!("Failed to spawn with cmd args {:?}: {}", args, e);
                        }
                    }
                }

                if let Some(proc) = spawned_child {
                    if let Some(state) = handle.try_state::<BackendProcess>() {
                        if let Ok(mut lock) = state.0.lock() {
                            *lock = Some(proc);
                        }
                    }
                } else {
                    eprintln!("CRITICAL: Could not start FastAPI backend with cmd /c python.");
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
