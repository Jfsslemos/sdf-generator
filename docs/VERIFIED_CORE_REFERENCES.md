# Referências verificadas — núcleo científico

Arquivo de apoio para posterior incorporação ao `.bib` da dissertação. As entradas abaixo foram conferidas contra páginas dos autores, proceedings, IEEE/CVF, NeurIPS ou DBLP. Não substitui a revisão final do estilo bibliográfico exigido pelo PPG.

## Entradas BibTeX

```bibtex
@inproceedings{mildenhall2020nerf,
  title     = {NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis},
  author    = {Mildenhall, Ben and Srinivasan, Pratul P. and Tancik, Matthew and Barron, Jonathan T. and Ramamoorthi, Ravi and Ng, Ren},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2020},
  eprint    = {2003.08934},
  archivePrefix = {arXiv}
}

@inproceedings{wang2023dmnerf,
  title     = {DM-NeRF: 3D Scene Geometry Decomposition and Manipulation from 2D Images},
  author    = {Wang, Bing and Chen, Lu and Yang, Bo},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023}
}

@inproceedings{wang2021neus,
  title     = {NeuS: Learning Neural Implicit Surfaces by Volume Rendering for Multi-view Reconstruction},
  author    = {Wang, Peng and Liu, Lingjie and Liu, Yuan and Theobalt, Christian and Komura, Taku and Wang, Wenping},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {34},
  year      = {2021}
}

@inproceedings{yariv2021volsdf,
  title     = {Volume Rendering of Neural Implicit Surfaces},
  author    = {Yariv, Lior and Gu, Jiatao and Kasten, Yoni and Lipman, Yaron},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2021}
}

@inproceedings{sucar2021imap,
  title     = {iMAP: Implicit Mapping and Positioning in Real-Time},
  author    = {Sucar, Edgar and Liu, Shikun and Ortiz, Joseph and Davison, Andrew J.},
  booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
  pages     = {6229--6238},
  year      = {2021},
  doi       = {10.1109/ICCV48922.2021.00617}
}

@inproceedings{zhu2022niceslam,
  title     = {NICE-SLAM: Neural Implicit Scalable Encoding for SLAM},
  author    = {Zhu, Zihan and Peng, Songyou and Larsson, Viktor and Xu, Weiwei and Bao, Hujun and Cui, Zhaopeng and Oswald, Martin R. and Pollefeys, Marc},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {12776--12786},
  year      = {2022},
  doi       = {10.1109/CVPR52688.2022.01245}
}

@inproceedings{kundu2022panoptic,
  title     = {Panoptic Neural Fields: A Semantic Object-Aware Neural Scene Representation},
  author    = {Kundu, Abhijit and Genova, Kyle and Yin, Xiaoqi and Fathi, Alireza and Pantofaru, Caroline and Guibas, Leonidas and Tagliasacchi, Andrea and Dellaert, Frank and Funkhouser, Thomas},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {12861--12871},
  year      = {2022},
  doi       = {10.1109/CVPR52688.2022.01253}
}
```

## Onde cada referência entra

| Chave | Papel na dissertação | Não usar para alegar |
|---|---|---|
| `mildenhall2020nerf` | definição/origem de NeRF e síntese de novas vistas | qualidade de geometria para simulação |
| `wang2023dmnerf` | método principal: reconstrução + decomposição por objeto + manipulação | contribuição original desta dissertação |
| `wang2021neus` | evidência de que reconstrução de superfície requer tratamento geométrico específico | baseline obrigatório |
| `yariv2021volsdf` | mesma discussão: densidade/radiance field não equivale a superfície explícita de alta fidelidade | baseline obrigatório |
| `sucar2021imap` | uso de representação neural implícita em robótica/SLAM | método diretamente comparável ao pipeline proposto |
| `zhu2022niceslam` | evolução de representação neural implícita para SLAM interno escalável | comparação quantitativa direta |
| `kundu2022panoptic` | representação neural orientada a objetos e separação things/stuff | substituto do DM-NeRF |

## Regra de posicionamento

A revisão deve distinguir três problemas: (1) síntese/reconstrução neural; (2) representação neural com estrutura geométrica ou orientada a objetos; e (3) conversão para geometria explícita estruturada destinada à simulação. A dissertação atua principalmente no terceiro, adotando DM-NeRF no primeiro/segundo. NeuS e VolSDF sustentam a distinção entre qualidade de renderização e superfície; iMAP/NICE-SLAM contextualizam robótica; Panoptic Neural Fields contextualiza estrutura orientada a objetos.

## Pendências bibliográficas

- Conferir o arquivo `.bib` já usado pela dissertação antes de copiar estas entradas, para evitar chaves duplicadas.
- Preferir a entrada ICLR 2023 de DM-NeRF no texto final; o README oficial ainda exibe uma entrada arXiv de 2022, apesar de o trabalho constar como ICLR 2023 no DBLP e na página do grupo.
- Não adicionar D-NeRF/NR-NeRF ao núcleo: cenas dinâmicas/deformáveis permanecem fora do escopo experimental.
