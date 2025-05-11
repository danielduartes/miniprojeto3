import Image from 'next/image';
import Head from 'next/head';
import logo from '../public/icone/logotrilhagram.png';
import { Manrope } from 'next/font/google';

const mainFontFamily = Manrope ({
  weight: ['700'],
  subsets: ['latin'],
});

export const metadata = {
  title: 'Login | Trilhagram',
  description: 'Página de login do Trilhagram',
};

export default function Home() {
  return (
    <>
      <Head>
        <title>Login | Trilhagram</title>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="shortcut icon" href="" type="image/x-icon" />
      </Head>

      <script type='module' src='assets/js/login.js'></script>

      <main className={`min-h-screen bg-[#FFFAF2] text-black ${mainFontFamily.className}`}>
        <header className="items-center">
          <h1 className="text-4xl text-center m-5 text-[#007698] py-5">Trilhagram</h1>
        </header>
        <div>
          <h2 className={`text-[2rem] text-center text-[#00AB5B] ${mainFontFamily.className}`}>Login</h2>
        </div>
        <div className="flex items-center justify-center min-h-screen -mt-[7.5rem] shadow-md">
          <section className="items-center w-60 p-6 m-4 space-y-5 rounded-md border-2 border-green-100 bg-[#CDF3D7] shadow-lg login">
            <form>
              <section>
                <div>
                  <label>Usuário</label>
                  <input type="text" name="usuário" id="user" className="bg-white text-start rounded-md px-1 border border-gray-500" required/>
                </div>
                <div>
                  <label>Senha</label>
                  <input type="password" name="senha" id="senha" className="bg-white rounded-md px-1 border border-gray-500" required/>
                </div>
              </section>
            </form>
            <div className="flex align-center justify-center">
              <button   type='submit' className="bg-[#00D468] rounded-lg px-4 text-white hover:ring-2 ring-blue-200 w-full hover:bg-green-900">
                <span className="text-justify">Entrar</span>
              </button>
            </div>
            <div className="text-center">
              <p className="align-center">Ainda não possui uma conta?</p>
              <a href="/" className="text-blue-400 hover:text-blue-600">Crie uma aqui</a>
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
