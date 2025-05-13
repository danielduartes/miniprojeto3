import { Fetcher } from "../fetcher.js"

export const Login = async () => {

    const response = await Fetcher({
        url: '/posts/all_posts',
        method: 'GET'
    })

    return `
        <form>
            <section className="items-center w-60 p-6 m-4 space-y-5 rounded-md border-2 border-green-100 bg-[#CDF3D7] shadow-lg">
              <section>
                  <div>
                    <label>Usuário</label>
                    <input type="text" name="usuário" id="user" className="bg-white text-start rounded-md px-1 border border-gray-500" required/>
                  </div>
                  <div>
                    <label>Senha</label>
                    <input type="password" name="senha" id="senha" className="bg-white rounded-md px-1 border border-gray-500" required/>
                  </div>
                  <div className="flex align-center justify-center">
                    <button type='submit' className="bg-[#00D468] rounded-lg px-4 text-white hover:ring-2 ring-blue-200 w-full hover:bg-green-900">
                      <span className="text-justify">Criar conta</span>
                    </button>
                  </div>
              </section>
          </section>
          </form>`

          component.querySelector('form').addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const data = Object.fromEntries(new FormData(ev.target).entries());

        const response = await Fetcher({
            url: '/users/login',
            method: 'POST',
            data: data
        })

        console.log(response)
    })

    return component;
}