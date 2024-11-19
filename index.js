const express = require("express");
const path = require("path");
const cadastroRoutes = require("./modules/cadastro/server");

const app = express();
const PORT = 3000;

// Middleware para interpretar JSON no body das requisições
app.use(express.json());

// Configura o servidor para servir arquivos estáticos da pasta 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Rota para o arquivo index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Usa as rotas do módulo de cadastro
app.use("/cadastro", cadastroRoutes);

// Inicializa o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
