import { Fetcher } from "../fetcher.js"

export const Register = async () => {

    const component = document.createElement('component')

    component.innerHTML = `
            <form>
              <div>
                <label>Usuário</label>
                <input type="text" name="usuário" id="user" className="bg-white text-start rounded-md px-1 border border-gray-500" required/>
              </div>
              <div>
                <label>E-mail</label>
                <input type="email" name="email" id="email" className="bg-white rounded-md px-1 w-full border border-gray-500" required/>
              </div>
              <div>
                <label>Senha</label>
                <input type="password" name="senha" id="senha" className="bg-white rounded-md px-1 border border-gray-500" required/>
              </div>
              <div className="flex items-center gap-2">
                <label className="text-xs justify-center">
                  <input type="checkbox" name="termos" className="appearance-none w-4 h-4 bg-white rounded-sm outline-none checked:bg-blue-500" id="termos" required/>
                  Aceite os Termos de Privacidade
                </label>
              </div>
            </form>
            `

    component.querySelector('form').addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const data = Object.fromEntries(new FormData(ev.target).entries());

        const response = await Fetcher({
            url: '/users/register',
            method: 'POST',
            data: data
        })

        console.log('register', response)
    })

    return component;
}