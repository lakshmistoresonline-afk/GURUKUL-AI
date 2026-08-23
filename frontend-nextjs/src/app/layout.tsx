import React from "react";
import type { Metadata, Viewport } from "next";
import "../styles/globals.css";
import { AuthProvider } from "../context/AuthContext";
import { LearningProvider } from "../context/LearningContext";

export const metadata: Metadata = {
  title: "Gurukul AI",
  description: "Personalized AI Learning Classroom",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background">
        <AuthProvider>
          <LearningProvider>
            {children}
          </LearningProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
