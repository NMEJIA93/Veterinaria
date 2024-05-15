const inputPrueba = document.querySelector('#prueba');
let checkMedicamentos = document.getElementById("med_pro");
let checkAyuda = document.getElementById("ayuda");
const opcMedicamentos = document.getElementById("medica1");
const opcProcedimientos = document.getElementById("procede1");
const checkboxProcedimientos = document.getElementById("procede");
const checkboxMedicamentos = document.querySelector("#medica");
const tablaMedicamento = document.querySelector('#medicamento1');
const tablaProcedimiento = document.querySelector('#procedimiento1');
const tablaAyuda = document.querySelector('#ayuda1');
const formularioHistoriaClinica = document.querySelector('#formularioConsulta');
const bntGrabar = document.querySelector('#btn_Grabar');
const inputAyudas = document.querySelector('#vectorAyudas')
const inputMedicamentos = document.querySelector('#vectorMedicamentos')
const inputProcedimientos = document.querySelector('#vectorProcedimientos')
const textAreaDiagnostico = document.querySelector('#diagnostico')


eventListeners();

function eventListeners() {
    document.addEventListener('DOMContentLoaded', () => {
        console.log("listo");

        checkMedicamentos.addEventListener("change", Med_Proc);
        checkAyuda.addEventListener("change", ayudaD);


        checkboxMedicamentos.addEventListener("change", () => {
            if (checkboxMedicamentos.checked && !checkboxProcedimientos.checked) {
                // Checkbox seleccionado
                console.log("va a enviar Medicamentos pero procedimientos no ");
                tablaMedicamento.style.display = 'block';
                tablaProcedimiento.style.display = 'none';
            }

            if (checkboxMedicamentos.checked && checkboxProcedimientos.checked) {
                tablaMedicamento.style.display = 'block';
                tablaProcedimiento.style.display = 'block';
            }

            if (!checkboxProcedimientos.checked && !checkboxMedicamentos.checked) {
                // Checkbox deseleccionado
                console.log("El checkbox no está seleccionado");
                tablaMedicamento.style.display = 'none';
                tablaProcedimiento.style.display = 'none';
            }
        });

        checkboxProcedimientos.addEventListener("change", () => {
            if (checkboxProcedimientos.checked && !checkboxMedicamentos.checked) {
                console.log("va a enviar procedimientos pero medicamentos no ");
                tablaMedicamento.style.display = 'none';
                tablaProcedimiento.style.display = 'block';
            }

            if (checkboxMedicamentos.checked && checkboxProcedimientos.checked) {
                tablaMedicamento.style.display = 'block';
                tablaProcedimiento.style.display = 'block';
            }

            if (!checkboxProcedimientos.checked && !checkboxMedicamentos.checked) {
                console.log("El checkbox no está seleccionado");
                tablaMedicamento.style.display = 'none';
                tablaProcedimiento.style.display = 'none';
            }
        });



        formularioHistoriaClinica.addEventListener('submit', (e) => {
            e.preventDefault()

            if (checkAyuda.checked == true) {
                //vector_ayudas();
                const vAyudas = vector_ayudas();
                if (vAyudas.length >= 1) {
                    inputAyudas.value = JSON.stringify(vAyudas);
                    formularioHistoriaClinica.submit();
                } else {
                    alert("si registra Ayuda Diagnostica debe seleccionar almenos 1")
                }

            }

            if (checkMedicamentos.checked == true && checkboxMedicamentos.checked == true && checkboxProcedimientos.checked == false) {
                const vMedicamentos = vector_Medicamentos();

                if (vMedicamentos.length >= 1) {
                    inputMedicamentos.value = JSON.stringify(vMedicamentos);
                    formularioHistoriaClinica.submit();
                    //console.log(JSON.stringify(vectorMedicamentos))
                    //console.log('se va a enviar vector Medicamentos')
                }
            }

            if (checkMedicamentos.checked == true && checkboxMedicamentos.checked == false && checkboxProcedimientos.checked == true) {
                const vprocedimientos = vector_Procedimientos();
                if (vprocedimientos.length >= 1) {
                    inputProcedimientos.value = JSON.stringify(vprocedimientos);
                    formularioHistoriaClinica.submit();
                } else {
                    alert("si registra Procedimientos debe seleccionar almenos 1")
                }
            }
            if (checkMedicamentos.checked == true && checkboxMedicamentos.checked == true && checkboxProcedimientos.checked == true) {
                vector_MedicamentosProcedimientos();
                const vMedicamentos = vector_Medicamentos();
                const vprocedimientos = vector_Procedimientos();
                if ((vMedicamentos.length > 0 || vprocedimientos.length > 0)) {
                    inputProcedimientos.value = JSON.stringify(vprocedimientos);
                    inputMedicamentos.value = JSON.stringify(vMedicamentos);
                    formularioHistoriaClinica.submit();
                }
            }
        })

    });
}

function vector_MedicamentosProcedimientos(e) {
    console.log('se va a enviar vector Medicamentos y Procedimientos')
}


function vector_Medicamentos(e) {
    const medicamentos = document.getElementById("Tmedica");
    const filas = medicamentos.querySelectorAll("tbody tr");
    const vectorMedicamentos = [];
    filas.forEach((fila) => {
        const columnas = fila.querySelectorAll("td");
        const codmedicamento = columnas[0].querySelector("#cod_medicamento").value;
        const dosis = columnas[2].querySelector("input[type='number']").value;
        const duracion = columnas[3].querySelector("input[type='number']").value;
        //const ayudas_seleccionadas = columnas[4].querySelector('#sel_ayuda').checked;
        const medicamentos_seleccionados = columnas[4].querySelector("input[type='checkbox']").checked;

        const objeto = {
            idMedicamento: codmedicamento,
            dosis: dosis,
            tiempoTratamiento: duracion
        };
        if (medicamentos_seleccionados) {
            vectorMedicamentos.push(objeto);
        }
    });
    return vectorMedicamentos;
}

function vector_Procedimientos(e) {
    const procedimientos = document.getElementById("Tprocede");
    const filas = procedimientos.querySelectorAll("tbody tr");
    const vectorProcedimientos = [];
    filas.forEach((fila) => {
        const columnas = fila.querySelectorAll("td");
        const codprocedimiento = columnas[0].querySelector("#cod_procede").value;
        const cantidad = columnas[2].querySelector("input[type='number']").value;
        const requiereEspecialista = columnas[3].querySelector("input[type='checkbox']").checked;
        //const ayudas_seleccionadas = columnas[4].querySelector('#sel_ayuda').checked;
        const procedimientos_seleccionados = columnas[4].querySelector("input[type='checkbox']").checked;

        const objeto = {
            idProcedimiento: codprocedimiento,
            cantidad: cantidad,
            asistenciaEspecializada: requiereEspecialista
        };
        if (procedimientos_seleccionados) {
            vectorProcedimientos.push(objeto);
        }
    });

    return vectorProcedimientos;
}


function vector_ayudas(e) {
    const ayudas = document.getElementById("tablaAyuda");
    const filas = ayudas.querySelectorAll("tbody tr");
    const vectorAyudas = [];

    filas.forEach((fila) => {
        const columnas = fila.querySelectorAll("td");
        const codayuda = columnas[0].querySelector("#cod_ayuda").value;
        const cantidad = columnas[2].querySelector("input[type='number']").value;
        const requiereEspecialista = columnas[3].querySelector("input[type='checkbox']").checked;
        //const ayudas_seleccionadas = columnas[4].querySelector('#sel_ayuda').checked;
        const ayudas_seleccionadas = columnas[4].querySelector("input[type='checkbox']").checked;

        const objeto = {
            ayuda: codayuda,
            cantidad: cantidad,
            requiereEspecialista: requiereEspecialista,
        };

        if (ayudas_seleccionadas) {
            vectorAyudas.push(objeto);
        }
    });

    /*     if (vectorAyudas.length >= 1) {
            inputAyudas.value = JSON.stringify(vAyudas);
            formularioHistoriaClinica.submit();
        } else {
            alert("si registra Ayuda Diagnostica debe seleccionar almenos 1")
        } */
    return vectorAyudas;
}


function Med_Proc(e) {
    e.preventDefault();
    if (checkMedicamentos.checked) {
        // inputPrueba.disabled = false;
        console.log("Seleccionó medicamentos y procedimientos");
        opcMedicamentos.style.pointerEvents = 'auto';
        opcProcedimientos.style.pointerEvents = 'auto';
        tablaAyuda.style.display = 'none'
        //tablaMedicamento.style.display = 'block';
        //tablaProcedimiento.style.display = 'block';
        opcMedicamentos.style.display = 'block'
        opcProcedimientos.style.display = 'block'
        //opcAyudas.style.display='none'
        textAreaDiagnostico.style.pointerEvents = 'auto';
    }
}



function ayudaD(e) {
    e.preventDefault();

    if (checkAyuda.checked) {
        // inputPrueba.disabled = false;
        tablaAyuda.style.display = 'block';
        console.log("Seleccionó ayuda");
        opcMedicamentos.style.pointerEvents = 'none';
        opcProcedimientos.style.pointerEvents = 'none';
        opcMedicamentos.style.display = 'none'
        opcProcedimientos.style.display = 'none'
        tablaMedicamento.style.display = 'none';
        tablaProcedimiento.style.display = 'none';
        textAreaDiagnostico.style.pointerEvents = 'none';
        checkboxProcedimientos.checked = false
        checkboxMedicamentos.checked = false
    }
}




function mostrarTablaContenido() {
    const radioAyuda = document.getElementById("ayuda");

    //const checkMedicamnetos = document.querySelector('#medica')
    if (radioAyuda.checked) {
        /*         const tablaAyuda = document.querySelector('tablaAyuda');
              
              if (tablaAyuda) {
                const filas = tabla.rows;
          
                for (let i = 0; i < filas.length; i++) {
                  const fila = filas[i];
                  const celdas = fila.cells;
          
                  for (let j = 0; j < celdas.length; j++) {
                    const celda = celdas[j];
                    const contenidoCelda = celda.innerHTML;
                    console.log("Contenido de la celda:", contenidoCelda);
                  }
                }
              } */
        inputPrueba.disabled = true
        console.log("ayuda seleccionada")
    } else {
        console.log("no seleccionada")
    }


}


