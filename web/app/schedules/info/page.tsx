import Image from 'next/image';
import Link from 'next/link';

function CollaboratorImage({ name, src }: { name: string, src: string }) {
    return (
        <div className="flex flex-col items-center justify-end text-center">
            {name}
            <br />
            <Link target='_blank' href={src.split('.png')[0]}>
                <Image
                    src={src}
                    alt={`Foto ${name}`}
                    width={100}
                    height={100}
                    className="rounded-full"
                />
            </Link>
        </div>

    );
}

const Team = () => {
    return (
        <div className="flex flex-col gap-5">
            <div className="grid grid-cols-3 gap-5">
                <CollaboratorImage name="Arthur Ribeiro" src="https://github.com/artrsousa1.png" />
                <CollaboratorImage name="Caio Habibe" src="https://github.com/CaioHabibe.png" />
                <CollaboratorImage name="Caio Rodrigues" src="https://github.com/caio-felipee.png" />
            </div>
        <div className="grid grid-cols-3 pb-10 gap-5">
                <CollaboratorImage name="Gabriel Castelo" src="https://github.com/GabrielCastelo-31.png" />
                <CollaboratorImage name="Henrique Camelo" src="https://github.com/henriquecq.png" />
                <CollaboratorImage name="Mateus Vieira" src="https://github.com/mateusvrs.png" />
            </div>
        </div>
    );
};

function About() {
    return (
        <>
            <h2 className="text-3xl font-semibold pb-5">Sobre</h2>
            <p className="text-justify">
                O Sua Grade UnB é um projeto em desenvolvimento da matéria de <b>Desenvolvimento de Software</b>.
                Seu propósito é proporcionar aos estudantes da Universidade de Brasília uma experiência simplificada e intuitiva na elaboração de suas grades horárias.
                O projeto visa facilitar o processo de organização acadêmica, oferecendo uma ferramenta eficiente e amigável para a montagem de horários, otimizando assim a gestão do tempo dos alunos.
            </p>
        </>
    );
}

function HowToUse() {
    return (
        <>
            <h2 className="text-3xl font-semibold pt-5 pb-5">Como utilizar?</h2>
            <p className="pb-5 text-justify">Na página inicial, clique no botão <b>Buscar Matéria</b> para selecionar as disciplinas desejadas para a sua grade. Escolha o ano/período e insira o nome da disciplina para poder optar por turmas potenciais na criação da grade, permitindo a escolha de até quatro turmas para cada disciplina.</p>
            <p className="pb-5 text-justify">Após fazer suas escolhas, clique no botão <b>Gerar Grade</b> e defina a prioridade dos turnos que melhor se adequam à sua rotina. Em seguida, basta escolher a grade mais adequada entre as opções geradas para realizar o download e/ou salvar as disciplinas escolhidas.</p>
            <p className="text-justify">Compartilhe suas experiências e sugestões. O aplicativo está em constante desenvolvimento, e seu feedback é valioso para aprimorar a experiência de todos os usuários.</p>
        </>
    );
}

function HowToContribute() {
    return (
        <>
            <h2 className="text-3xl font-semibold  pt-5 pb-5">Como contribuir?</h2>
            <p className="text-justify">
                Se você é um programador e deseja contribuir com nosso projeto, basta <Link legacyBehavior href="https://unb-mds.github.io/2023-2-Squad11/contributing/" className=""><a target="_blank" className="text-primary hover:underline">clicar aqui</a></Link> para ter acesso a nossa documentação. Lá você encontrará todos os detalhes de como contribuir com novas funcionalidades e reportar possíveis erros.
            </p>
        </>
    );
}

function Collaborators() {
    return (
        <>
            <h2 className="text-3xl font-semibold  pt-5 pb-5">Colaboradores</h2>
            <Team />
        </>
    );
}

export default function Info() {

    return (
        <div className="overflow-auto m-auto min-h-full max-h-full px-8 max-w-4xl">
            <div className="flex flex-col items-center gap-5 py-0">
                <div className="flex flex-col items-center gap-2">
                    <About />
                    <HowToUse />
                    <HowToContribute />
                    <Collaborators />
                </div>
            </div>
        </div>
    );
}