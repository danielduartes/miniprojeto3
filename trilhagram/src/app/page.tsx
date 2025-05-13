"use client";

import Image from 'next/image';
import Head from 'next/head';
import Link from 'next/link';
import logo from '../public/icone/logotrilhagram.png';
import { useState } from 'react';
import { useRouter } from 'next/navigation';


export default function create_user() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);
  setError('');

  try {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: name, // Corrigido
        email_user: email, // Corrigido
        password_user: password // Corrigido
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro no registro'); // .detail em vez de .message
    }

    router.push('/login');
  } catch (err) {
    if (err instanceof Error) {
      setError(err.message);
    } else {
      setError('Erro desconhecido');
    }
  } finally {
    setLoading(false);
  }
};


  return (
    <>
      <Head>
        <title>Registro | Trilhagram</title>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="shortcut icon" href="" type="image/x-icon" />
      </Head>

      <main className="min-h-screen bg-[#FFFAF2] text-black font-bold">
        <header className="items-center">
          <h1 className="text-4xl text-center m-5 text-[#007698] py-5">Trilhagram</h1>
        </header>
        <div>
          <h2 className="text-[2rem] text-center text-[#00AB5B]">Registro</h2>
        </div>
        <div className="flex items-center justify-center min-h-screen -mt-[7.5rem] shadow-md">
          <section className="items-center w-60 p-6 m-4 space-y-5 rounded-md border-2 border-green-100 bg-[#CDF3D7] shadow-lg">
            <form onSubmit={create_user}>
              <div>
                <label>Usuário</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="bg-white text-start rounded-md px-1 border border-gray-500 w-full"
                  required
                />
              </div>
              <div>
                <label>E-mail</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-white rounded-md px-1 w-full border border-gray-500"
                  required
                />
              </div>
              <div>
                <label>Senha</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-white rounded-md px-1 border border-gray-500 w-full"
                  required
                />
              </div>
              <div className="flex items-center gap-2">
                <label className="text-xs justify-center m-3">
                  <input
                    type="checkbox"
                    name="termos"
                    className="appearance-none w-4 h-4 bg-white rounded-sm outline-none checked:bg-blue-500 mx-3"
                    required
                  />
                  Aceite os Termos de Privacidade
                </label>
              </div>
              <div className="flex justify-center mt-4">
                <button
                  type="submit"
                  className="bg-[#00D468] rounded-lg px-4 text-white hover:ring-2 ring-blue-200 w-full hover:bg-green-900"
                >
                  {loading ? 'Criando conta...' : 'Criar conta'}
                </button>
              </div>
              {error && <p className="text-red-500 text-sm text-center">{error}</p>}
            </form>
            <div className="text-center">
              <p className="align-center">Já possui uma conta?</p>
              <Link href="/login" className="text-blue-400 hover:text-blue-600">
                Conecte-se
              </Link>
            </div>
          </section>
        </div>

        <footer className="text-xs text-center justify-items-center p-5 space-y-4">
          <p>
            <a href="https://trilhaufpb.com" target="_blank" className="hover:underline">
              Trilha UFPB
            </a>
          </p>
          <p>&copy; 2025 Trilhagram. Todos os direitos reservados</p>
          <p>Desenvolvido por: Pedro, Daniel, Filipe e Vinícius</p>
        </footer>
      </main>
    </>
  );
}
