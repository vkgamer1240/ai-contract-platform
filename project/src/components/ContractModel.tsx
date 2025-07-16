import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh } from 'three';

export function ContractModel() {
  const meshRef = useRef<Mesh>(null!);

  useFrame((state, delta) => {
    meshRef.current.rotation.y += delta * 0.5;
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[2, 3, 0.2]} />
      <meshStandardMaterial color="#4F46E5" metalness={0.5} roughness={0.5} />
    </mesh>
  );
}