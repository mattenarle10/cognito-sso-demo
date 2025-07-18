"use client"

import { useState, useEffect } from "react"
import { Canvas } from "@react-three/fiber"
import { OrbitControls, Environment } from "@react-three/drei"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { ChevronDown, User, ShoppingBag, LogOut } from "lucide-react"
import Link from "next/link"
import { AbstractShapes } from "@/components/abstract-shapes"

const mockUser = {
  name: "Alex Johnson",
  email: "alex@example.com",
}

export default function LandingPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState<typeof mockUser | null>(null)

  useEffect(() => {
    const checkAuth = () => {
      const authStatus = localStorage.getItem("isLoggedIn")
      if (authStatus === "true") {
        setIsLoggedIn(true)
        setUser(mockUser)
      }
    }
    checkAuth()
  }, [])

  const handleSignIn = () => {
    setIsLoggedIn(true)
    setUser(mockUser)
    localStorage.setItem("isLoggedIn", "true")
  }

  const handleSignOut = () => {
    setIsLoggedIn(false)
    setUser(null)
    localStorage.removeItem("isLoggedIn")
  }

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 px-8 py-6">
        <nav className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="text-2xl font-light tracking-[0.2em]">THE GRIND</div>

          <div className="flex items-center">
            {isLoggedIn && user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="text-white hover:bg-white/10 font-light">
                    Hello, {user.name.split(" ")[0]}
                    <ChevronDown className="ml-2 h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="bg-zinc-900 border-zinc-800 text-white">
                  <DropdownMenuItem asChild className="hover:bg-zinc-800">
                    <Link href="/profile" className="flex items-center">
                      <User className="mr-2 h-4 w-4" />
                      Profile
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild className="hover:bg-zinc-800">
                    <Link href="/orders" className="flex items-center">
                      <ShoppingBag className="mr-2 h-4 w-4" />
                      Orders
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleSignOut} className="hover:bg-zinc-800">
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <Button
                onClick={handleSignIn}
                variant="outline"
                className="border-white/20 text-white hover:bg-white hover:text-black transition-all duration-300 font-light bg-transparent"
              >
                Sign In
              </Button>
            )}
          </div>
        </nav>
      </header>

      {/* 3D Background */}
      <div className="fixed inset-0">
        <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
          <Environment preset="night" />
          <ambientLight intensity={0.2} />
          <directionalLight position={[10, 10, 5]} intensity={0.5} />
          <AbstractShapes />
          <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.2} />
        </Canvas>
      </div>

      {/* Main Content */}
      <main className="relative z-10 flex items-center justify-center min-h-screen px-8">
        <div className="text-center max-w-6xl mx-auto">
          <div className="space-y-12">
            <div className="space-y-8">
              <h1 className="text-[6rem] md:text-[8rem] font-thin tracking-[-0.02em] leading-none">THE</h1>
              <h1 className="text-[6rem] md:text-[8rem] font-thin tracking-[-0.02em] leading-none -mt-6">GRIND</h1>
            </div>

            <div className="w-px h-24 bg-white/20 mx-auto"></div>

            <div className="space-y-8">
              <p className="text-xl md:text-2xl font-light tracking-[0.1em] text-white/60 max-w-2xl mx-auto">
                PREMIUM MEMBERSHIP
              </p>

              {!isLoggedIn ? (
                <div className="flex justify-center">
                  <Button
                    onClick={handleSignIn}
                    className="bg-white text-black hover:bg-white/90 px-12 py-4 text-lg font-light tracking-[0.1em] transition-all duration-300 transform hover:scale-105"
                  >
                    ENTER
                  </Button>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="text-4xl md:text-6xl font-thin tracking-[-0.02em]">WELCOME BACK</div>
                  <div className="flex gap-6 justify-center items-center">
                    <Link href="/orders">
                      <Button className="bg-white text-black hover:bg-white/90 px-8 py-3 font-light tracking-[0.1em]">
                        ORDERS
                      </Button>
                    </Link>
                    <Link href="/profile">
                      <Button
                        variant="outline"
                        className="border-white/20 text-white hover:bg-white hover:text-black px-8 py-3 font-light tracking-[0.1em] bg-transparent"
                      >
                        PROFILE
                      </Button>
                    </Link>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Floating Elements */}
      <div className="fixed top-1/4 left-8 w-2 h-2 bg-white/10 rounded-full animate-pulse"></div>
      <div className="fixed top-1/3 right-12 w-1 h-1 bg-white/20 rounded-full animate-bounce"></div>
      <div className="fixed bottom-1/4 left-16 w-3 h-3 bg-white/5 rounded-full animate-pulse delay-1000"></div>
      <div className="fixed bottom-1/3 right-8 w-1 h-1 bg-white/15 rounded-full animate-bounce delay-500"></div>
    </div>
  )
}
