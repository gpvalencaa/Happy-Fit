// const express = require("express");
// const fs = require("fs");
// const path = require("path");
// const app = express();
// const PORT = 3000;

// // Middleware para interpretar JSON no body das requisições
// app.use(express.json());

// // Configura o servidor para servir arquivos estáticos da pasta 'public'
// app.use(express.static(path.join(__dirname, 'public')));

// // Rota para servir o index.html na raiz
// app.get('/', (req, res) => {
//   res.sendFile(path.join(__dirname, 'public', 'index.html'));
// });

// // Rota para o cadastro de usuários
// app.post("/api/cadastrar", (req, res) => {
//     const { nome, idade, peso, email, sexo, altura, senha } = req.body;
  
//     // Validar se todos os campos foram preenchidos
//     if (!nome || !idade || !peso || !email || !sexo || !altura || !senha) {
//       return res.status(400).json({ message: "Por favor, preencha todos os campos." });
//     }
  
//     // Caminho do arquivo JSON
//     const filePath = path.join(__dirname, "data", "usuarios.json");
  
//     // Carregar os dados existentes
//     let dados = [];
//     if (fs.existsSync(filePath)) {
//       const dadosExistentes = fs.readFileSync(filePath);
      
//       // Verifica se o arquivo está vazio
//       if (dadosExistentes.length === 0) {
//           console.log('Arquivo vazio, criando o arquivo com o primeiro usuário...');
          
//           // Inicializa o array de usuários com o primeiro usuário
//           dados = [];
          
//           // Escreve o primeiro usuário no arquivo
//           fs.writeFileSync(filePath, JSON.stringify(dados, null, 2));
//           console.log('Primeiro usuário adicionado com sucesso!');
//       } else {
//           // Caso já existam dados no arquivo
//           console.log('Arquivo não está vazio, carregando dados...');
//           dados = JSON.parse(dadosExistentes);
//       }
//     } else {
//       // Se o arquivo não existe, cria um novo arquivo e adiciona o primeiro usuário
//       console.log('Arquivo não encontrado, criando um novo arquivo com o primeiro usuário...');
      
//       dados = [{ nome, idade, peso, email, sexo, altura, senha }];
      
//       fs.writeFileSync(filePath, JSON.stringify(dados, null, 2));
//       console.log('Arquivo criado e primeiro usuário adicionado com sucesso!');
//     }
  
//     // Adicionar o novo usuário ao array de dados
//     dados.push({ nome, idade, peso, email, sexo, altura, senha });
  
//     // Salvar os dados no arquivo JSON
//     fs.writeFileSync(filePath, JSON.stringify(dados, null, 2));
  
//     res.status(201).json({ message: "Usuário cadastrado com sucesso!" });
//   });
  

// // Inicializa o servidor
// app.listen(PORT, () => {
//   console.log(`Servidor rodando em http://localhost:${PORT}`);
// });


// const express = require("express");
// const fs = require("fs");
// const path = require("path");
// const router = express.Router();

// // Rota para o cadastro de usuários
// router.post("/api/cadastrar", (req, res) => {
//   const { nome, idade, peso, email, sexo, altura, senha } = req.body;

//   // Validar se todos os campos foram preenchidos
//   if (!nome || !idade || !peso || !email || !sexo || !altura || !senha) {
//     return res.status(400).json({ message: "Por favor, preencha todos os campos." });
//   }

//   // Caminho do arquivo JSON
//   const filePath = path.join(__dirname, "../../data", "usuarios.json");

//   // Carregar os dados existentes
//   let dados = [];
//   if (fs.existsSync(filePath)) {
//     const dadosExistentes = fs.readFileSync(filePath);
    
//     // Verifica se o arquivo está vazio
//     if (dadosExistentes.length === 0) {
//       console.log('Arquivo vazio, criando o arquivo com o primeiro usuário...');
//       dados = [];
//       fs.writeFileSync(filePath, JSON.stringify(dados, null, 2));
//       console.log('Primeiro usuário adicionado com sucesso!');
//     } else {
//       console.log('Arquivo não está vazio, carregando dados...');
//       dados = JSON.parse(dadosExistentes);
//     }
//   } else {
//     console.log('Arquivo não encontrado, criando um novo arquivo com o primeiro usuário...');
//     dados = [{ nome, idade, peso, email, sexo, altura, senha }];
//     fs.writeFileSync(filePath, JSON.stringify(dados, null, 2));
//     console.log('Arquivo criado e primeiro usuário adicionado com sucesso!');
//   }

//   // Adicionar o novo usuário ao array de dados
//   dados.push({ nome, idade, peso, email, sexo, altura, senha });

//   // Salvar os dados no arquivo JSON
//   fs.writeFileSync(filePath, JSON.stringify(dados, null, 2));

//   res.status(201).json({ message: "Usuário cadastrado com sucesso!" });
// });

// module.exports = router;

const express = require("express");
const fs = require("fs");
const path = require("path");

const router = express.Router();

// Rota para o cadastro de usuários
router.post("/cadastrar", (req, res) => {
  const { nome, idade, peso, email, sexo, altura, senha } = req.body;

  // Validar se todos os campos foram preenchidos
  if (!nome || !idade || !peso || !email || !sexo || !altura || !senha) {
    return res.status(400).json({ message: "Por favor, preencha todos os campos." });
  }

  // Caminho do arquivo JSON
  const filePath = path.join(__dirname, "../../data", "usuarios.json");

  // Carregar os dados existentes
  let dados = [];
  try {
    if (fs.existsSync(filePath)) {
      const dadosExistentes = fs.readFileSync(filePath, "utf-8");

      // Verifica se o arquivo está vazio
      if (dadosExistentes.length === 0) {
        console.log('Arquivo vazio, criando o arquivo com o primeiro usuário...');
        dados = [];
      } else {
        // Caso já existam dados no arquivo
        console.log('Arquivo não está vazio, carregando dados...');
        dados = JSON.parse(dadosExistentes);
      }
    } else {
      console.log('Arquivo não encontrado, criando um novo arquivo com o primeiro usuário...');
      dados = [];
    }
  } catch (error) {
    console.error('Erro ao ler ou processar o arquivo JSON:', error);
    return res.status(500).json({ message: "Erro ao acessar o arquivo de dados." });
  }

  // Adicionar o novo usuário ao array de dados
  dados.push({ nome, idade, peso, email, sexo, altura, senha });

  try {
    // Salvar os dados no arquivo JSON
    fs.writeFileSync(filePath, JSON.stringify(dados, null, 2));
    console.log('Dados atualizados no arquivo JSON!');
  } catch (error) {
    console.error('Erro ao escrever no arquivo JSON:', error);
    return res.status(500).json({ message: "Erro ao salvar os dados." });
  }

  res.status(201).json({ message: "Usuário cadastrado com sucesso!" });
});

module.exports = router;

