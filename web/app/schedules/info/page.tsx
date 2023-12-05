'use client';

import useUser from '@/app/hooks/useUser';

import Image from 'next/image';
import Link from 'next/link';

const Team = () => {
    return (
        <div className="flex flex-col gap-5">
            <div className="flex gap-5">
                <div className="text-center">
                    Arthur Ribeiro
                    <br/>
                    <Image
                        src="https://github.com/artrsousa1.png"
                        alt="Foto Arthur"
                        width={100}
                        height={100}
                        className="rounded-full"
                    />
                </div>
                <div className="text-center">
                    Caio Habibe
                    <br/>
                    <Image
                        src="https://github.com/CaioHabibe.png"
                        alt="Foto Caio Habibe"
                        width={100}
                        height={100}
                        className="rounded-full"
                    />
                </div>
                <div className="text-center">
                    Caio Felipe
                    <br/>
                    <Image
                        src="https://github.com/caio-felipee.png"
                        alt="Foto Caio Felipe"
                        width={100}
                        height={100}
                        className="rounded-full"
                    />
                </div>
            </div>
            <div className="flex gap-5">
                <div className="text-center">
                    Gabriel Castelo
                    <br/>
                    <Image
                        src="https://github.com/GabrielCastelo-31.png"
                        alt="Foto Gabriel"
                        width={100}
                        height={100}
                        className="rounded-full"
                    />
                </div>
                <div className="text-center">
                    Henrique Camelo
                    <br/>
                    <Image
                        src="https://github.com/henriquecq.png"
                        alt="Foto Henrique"
                        width={100}
                        height={100}
                        className="rounded-full"
                    />
                </div>
                <div className="text-center">
                    Mateus Vieira
                    <br/>
                    <Image
                        src="https://github.com/mateusvrs.png"
                        alt="Foto Mateus"
                        width={100}
                        height={100}
                        className="rounded-full"
                    />
                </div>
            </div>
        </div>
    );
};

export default function Info() {
    const { user } = useUser();

    return (
        <div className="overflow-auto m-auto min-h-full max-h-full px-8 max-w-4xl">
            <div className="flex flex-col items-center gap-5 py-0">
                <div className="flex flex-col items-center gap-2">
                    <h2 className="text-3xl font-semibold pb-5">Sobre</h2>
                    <p className="text-justify">
                        O Sua Grade UnB é um projeto em desenvolvimento da matéria de <b>Desenvolvimento de Software</b>.
                        Seu propósito é proporcionar aos estudantes da Universidade de Brasília uma experiência simplificada e intuitiva na elaboração de suas grades horárias.
                        O projeto visa facilitar o processo de organização acadêmica, oferecendo uma ferramenta eficiente e amigável para a montagem de horários, otimizando assim a gestão do tempo dos alunos.
                    </p>
                    <h2 className="text-3xl font-semibold pt-5 pb-5">Como utilizar?</h2>
                    <p className="text-justify">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Eum nemo repellat voluptas culpa qui ullam dolorem laudantium aliquam dolorum,
                        ex est nulla labore expedita repellendus ab harum sequi doloribus fugiat.
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Eum nemo repellat voluptas culpa qui ullam dolorem laudantium aliquam dolorum,
                        ex est nulla labore expedita repellendus ab harum sequi doloribus fugiat.
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Eum nemo repellat voluptas culpa qui ullam dolorem laudantium aliquam dolorum,
                        ex est nulla labore expedita repellendus ab harum sequi doloribus fugiat.
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Eum nemo repellat voluptas culpa qui ullam dolorem laudantium aliquam dolorum,
                        ex est nulla labore expedita repellendus ab harum sequi doloribus fugiat.
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Eum nemo repellat voluptas culpa qui ullam dolorem laudantium aliquam dolorum,
                        ex est nulla labore expedita repellendus ab harum sequi doloribus fugiat.
                    </p>
                    <h2 className="text-3xl font-semibold  pt-5 pb-5">Como contribuir?</h2>
                    <p className="text-justify">
                        Se você é um programador e deseja contribuir com nosso projeto, basta <Link legacyBehavior href="https://unb-mds.github.io/2023-2-Squad11/contributing/" className=""><a target="_blank" className="text-primary hover:underline">clicar aqui</a></Link> para ter acesso a nossa documentação. Lá você encontrará todos os detalhes de como contribuir com novas funcionalidades e reportar possíveis erros.
                    </p>
                    <h2 className="text-3xl font-semibold  pt-5 pb-5">Colaboradores</h2>
                    <Team />
                </div>
            </div>
        </div>
    );
}