"use client"

import { useRef } from "react"
import { useFrame } from "@react-three/fiber"
import { Float } from "@react-three/drei"
import type * as THREE from "three"

function CoffeeBean({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) {
  const meshRef = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.1
      meshRef.current.rotation.y += 0.01
    }
  })

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
      <mesh ref={meshRef} position={position} scale={scale}>
        {/* Coffee bean shape using two spheres */}
        <group>
          <mesh position={[0, 0.1, 0]}>
            <sphereGeometry args={[0.3, 16, 16]} />
            <meshStandardMaterial color="#8B4513" roughness={0.8} metalness={0.1} />
          </mesh>
          <mesh position={[0, -0.1, 0]}>
            <sphereGeometry args={[0.3, 16, 16]} />
            <meshStandardMaterial color="#8B4513" roughness={0.8} metalness={0.1} />
          </mesh>
          {/* Coffee bean crack */}
          <mesh position={[0, 0, 0.25]} rotation={[0, 0, Math.PI / 4]}>
            <boxGeometry args={[0.05, 0.6, 0.1]} />
            <meshStandardMaterial color="#654321" />
          </mesh>
        </group>
      </mesh>
    </Float>
  )
}

export function CoffeeBeans() {
  return (
    <group>
      <CoffeeBean position={[-8, 4, -5]} scale={1.2} />
      <CoffeeBean position={[6, -3, -8]} scale={0.8} />
      <CoffeeBean position={[-4, -6, -3]} scale={1.5} />
      <CoffeeBean position={[8, 2, -6]} scale={1.0} />
      <CoffeeBean position={[-6, 6, -10]} scale={0.9} />
      <CoffeeBean position={[4, 8, -4]} scale={1.1} />
      <CoffeeBean position={[-2, -8, -7]} scale={1.3} />
      <CoffeeBean position={[10, -5, -9]} scale={0.7} />
    </group>
  )
}
