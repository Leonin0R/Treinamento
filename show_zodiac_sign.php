<?php include('header.php'); ?>

<main class="container my-5 flex-grow-1" style="position: relative; z-index: 10;">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <?php
            // 1. Verifica se a data de nascimento foi enviada via POST
            if (isset($_POST['data_nascimento']) && !empty($_POST['data_nascimento'])) {
                
                $data_nascimento_str = $_POST['data_nascimento']; 
                $signos_xml = simplexml_load_file('signos.xml');
                
                $data_nascimento_obj = new DateTime($data_nascimento_str);
                $ano_nascimento = $data_nascimento_obj->format('Y'); 
                
                $signo_encontrado = null;
                $caracteristicas_array = []; // Array para armazenar as frases
                
                // 4. Itera sobre cada signo no XML
                foreach ($signos_xml->signo as $signo) {
                    // Lógica de Datas (CORRIGIDA)
                    $data_inicio_str = (string)$signo->dataInicio;
                    $data_fim_str = (string)$signo->dataFim;
                    $data_inicio = DateTime::createFromFormat('d/m/Y', $data_inicio_str . '/' . $ano_nascimento);
                    $data_fim = DateTime::createFromFormat('d/m/Y', $data_fim_str . '/' . $ano_nascimento);

                    if ($data_inicio > $data_fim) {
                        $data_fim->modify('+1 year');
                        if ($data_nascimento_obj < $data_inicio) {
                            $data_nascimento_obj->modify('+1 year');
                        }
                    }

                    // 5. Compara e, se encontrar, armazena as frases
                    if ($data_nascimento_obj >= $data_inicio && $data_nascimento_obj <= $data_fim) {
                        $signo_encontrado = $signo;
                        
                        // NOVO: Armazena todas as frases na array
                        foreach ($signo->caracteristicas->frase as $frase) {
                            $caracteristicas_array[] = (string)$frase;
                        }
                        break;
                    }
                    $data_nascimento_obj = new DateTime($data_nascimento_str); // Reseta o ano
                }

                // 6. Exibe o resultado
                if ($signo_encontrado) {
                    echo "<div class='card card-signo shadow-lg text-center p-4 bg-primary text-white'>"; 
                    echo "<h2 class='card-title display-4 fw-bold'>Seu Signo é: " . $signo_encontrado->signoNome . "!</h2>";
                    
                    echo "<img src='" . $signo_encontrado->imagem . "' alt='Símbolo de " . $signo_encontrado->signoNome . "' class='img-fluid rounded-circle my-4 signo-img shadow'>";
                    
                    // NOVO: Div que receberá a descrição cíclica pelo JavaScript
                    echo "<p class='lead' id='descricao-ciclica'></p>";
                    
                    echo "<p class='text-muted' style='color: rgba(255, 255, 255, 0.7) !important;'>Período: " . $signo_encontrado->dataInicio . " a " . $signo_encontrado->dataFim . "</p>";
                    echo "</div>";
                } else {
                    echo "<div class='alert alert-warning text-center'>Não foi possível determinar seu signo. Verifique se a data está correta.</div>";
                }

            } else {
                echo "<div class='alert alert-danger text-center'>Nenhuma data de nascimento foi fornecida.</div>";
            }
            ?>
            <div class="text-center mt-4">
                <a href="index.php" class="btn btn-secondary btn-lg">Voltar à página inicial</a>
            </div>
        </div>
    </div>
</main>

<footer class="mt-auto bg-dark text-white text-center p-3" style="position: relative; z-index: 10;">
    <p class="mb-0">Desenvolvido como atividade prática.</p>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlIza9/sU5T7iC7v/9p01+6k/9rD5w/G9m8I7uH6J8A" crossorigin="anonymous"></script>

<script>
    <?php
    // Passa o array de frases do PHP para uma variável JavaScript
    if (!empty($caracteristicas_array)) {
        echo "const frases = " . json_encode($caracteristicas_array) . ";";
    } else {
        echo "const frases = ['Erro: Descrições não encontradas no XML.'];";
    }
    ?>

    let fraseIndex = 0;
    const elementoDescricao = document.getElementById('descricao-ciclica');
    const tempoDeExibicao = 4000; // 4 segundos visível
    const tempoDeTransicao = 500;  // 0.5 segundos para fade

    function mudarFrase() {
        if (!elementoDescricao || frases.length === 0) return;

        // 1. Inicia o Fade-Out
        elementoDescricao.style.opacity = 0;
        
        setTimeout(() => {
            // 2. Muda o texto após o Fade-Out
            elementoDescricao.textContent = frases[fraseIndex];
            
            // 3. Inicia o Fade-In
            elementoDescricao.style.opacity = 1;
            
            // 4. Avança para a próxima frase
            fraseIndex = (fraseIndex + 1) % frases.length;
        }, tempoDeTransicao);
    }

    // Aplica a transição CSS (para que o fade funcione)
    if (elementoDescricao) {
        elementoDescricao.style.transition = `opacity ${tempoDeTransicao / 1000}s ease-in-out`;
        mudarFrase(); // Exibe a primeira frase imediatamente
        setInterval(mudarFrase, tempoDeExibicao); // Repete a cada 4 segundos
    }
</script>

</body>
</html>