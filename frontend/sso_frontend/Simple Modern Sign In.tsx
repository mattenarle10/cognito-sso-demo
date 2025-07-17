"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import Link from "next/link"
import { Coffee, Mail, Lock, ArrowRight } from "lucide-react"

export default function SignIn() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-950 via-black to-zinc-950 relative overflow-hidden">
      {/* Multiple sophisticated background textures */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.03),transparent)]" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_80%_80%,rgba(120,119,198,0.02),transparent)]" />
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]" />

      {/* Noise texture overlay - simplified */}
      <div
        className="absolute inset-0 opacity-[0.015]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Subtle floating coffee beans pattern */}
      <div className="absolute inset-0 opacity-[0.02]">
        <div className="absolute top-20 left-20">
          <Coffee size={12} className="text-white rotate-12" />
        </div>
        <div className="absolute top-40 right-32">
          <Coffee size={8} className="text-white -rotate-45" />
        </div>
        <div className="absolute bottom-32 left-16">
          <Coffee size={10} className="text-white rotate-90" />
        </div>
        <div className="absolute bottom-20 right-20">
          <Coffee size={14} className="text-white -rotate-12" />
        </div>
      </div>

      {/* Main container - centered layout */}
      <div className="min-h-screen flex items-center justify-center p-8">
        <div className="w-full max-w-md relative">
          {/* Form container with enhanced textures */}
          <div className="relative">
            {/* Multiple glow effects */}
            <div className="absolute -inset-2 bg-gradient-to-r from-zinc-800/20 to-neutral-800/20 rounded-3xl blur-xl" />
            <div className="absolute -inset-1 bg-gradient-to-br from-zinc-700/10 to-zinc-900/10 rounded-3xl blur-lg" />

            <div className="relative bg-gradient-to-b from-zinc-900/95 to-black/98 backdrop-blur-xl border border-zinc-800/60 rounded-2xl p-8 lg:p-10 overflow-hidden">
              {/* Card texture overlays */}
              <div className="absolute inset-0 bg-gradient-to-br from-zinc-800/5 via-transparent to-zinc-900/10 rounded-2xl" />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.01)_0%,transparent_50%)]" />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(255,255,255,0.008)_0%,transparent_50%)]" />

              {/* Subtle grain texture on card */}
              <div
                className="absolute inset-0 opacity-[0.03] rounded-2xl"
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='cardNoise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' seed='1' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23cardNoise)'/%3E%3C/svg%3E")`,
                }}
              />

              {/* Subtle border highlight */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-transparent via-zinc-600/20 to-transparent p-[1px]">
                <div className="w-full h-full bg-transparent rounded-2xl" />
              </div>

              <div className="relative z-10">
                {/* Header section with subtle icon */}
                <div className="mb-12 relative">
                  <div className="absolute -top-2 -right-2 opacity-5">
                    <Coffee size={80} className="text-white" />
                  </div>
                  <h1 className="text-4xl lg:text-5xl font-medium tracking-tight text-white mb-4 bg-gradient-to-r from-white via-zinc-100 to-zinc-300 bg-clip-text text-transparent relative">
                    The Grind
                  </h1>
                  <p className="text-zinc-400 font-light tracking-wide">Welcome back to your coffee journey</p>
                </div>

                {/* Form with enhanced styling */}
                <form className="space-y-8">
                  <div className="space-y-3 relative">
                    <Label
                      htmlFor="email"
                      className="text-zinc-300 font-medium tracking-wide text-sm block flex items-center gap-2"
                    >
                      <Mail size={14} className="text-zinc-500" />
                      Email Address
                    </Label>
                    <div className="relative">
                      <Input
                        id="email"
                        type="email"
                        placeholder="your@email.com"
                        className="bg-zinc-900/60 border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-14 rounded-xl font-light tracking-wide text-base transition-all duration-200 pl-4 relative"
                        required
                      />
                      {/* Input field texture */}
                      <div className="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-xl pointer-events-none" />
                    </div>
                  </div>

                  <div className="space-y-3 relative">
                    <Label
                      htmlFor="password"
                      className="text-zinc-300 font-medium tracking-wide text-sm block flex items-center gap-2"
                    >
                      <Lock size={14} className="text-zinc-500" />
                      Password
                    </Label>
                    <div className="relative">
                      <Input
                        id="password"
                        type="password"
                        placeholder="Enter your password"
                        className="bg-zinc-900/60 border-zinc-700/60 text-white placeholder:text-zinc-500 focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400 h-14 rounded-xl font-light tracking-wide text-base transition-all duration-200 pl-4 relative"
                        required
                      />
                      {/* Input field texture */}
                      <div className="absolute inset-0 bg-gradient-to-r from-zinc-800/5 to-transparent rounded-xl pointer-events-none" />
                    </div>
                  </div>

                  <Button
                    type="submit"
                    className="w-full bg-gradient-to-r from-zinc-700 to-zinc-800 hover:from-zinc-600 hover:to-zinc-700 text-white font-medium tracking-wide py-4 h-14 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl border border-zinc-600/30 group relative overflow-hidden"
                  >
                    {/* Button texture */}
                    <div className="absolute inset-0 bg-gradient-to-r from-zinc-600/10 via-transparent to-zinc-800/10" />
                    <span className="group-hover:tracking-wider transition-all duration-200 flex items-center justify-center gap-2 relative z-10">
                      Sign In
                      <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform duration-200" />
                    </span>
                  </Button>
                </form>

                {/* Footer with better styling */}
                <div className="mt-10 pt-8 border-t border-zinc-800/50 relative">
                  {/* Border texture */}
                  <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-zinc-700/30 to-transparent" />
                  <p className="text-center text-zinc-400 font-light">
                    New to The Grind?{" "}
                    <Link
                      href="/signup"
                      className="text-zinc-200 hover:text-white font-medium underline underline-offset-4 decoration-zinc-600 hover:decoration-zinc-400 transition-all duration-200 inline-flex items-center gap-1"
                    >
                      Create your account
                      <ArrowRight size={12} className="opacity-60" />
                    </Link>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
