(defrule perfil-basico
(or (and (programacion SI)(administracion NO)(redes NO)(tecnologia NO) )
(and (redes SI)(administracion NO)(tecnologia NO)(programacion NO) )
(and (administracion SI) (programacion NO)(redes NO)(tecnologia NO) )
(and (tecnologia SI) (administracion NO) (programacion NO) (administracion NO) ))
=>
(assert (perfil basico))
)

(defrule perfil-completo
(programacion SI)
(redes SI)
(administracion SI)
(tecnologia SI)
=>
(assert (perfil completo))
)

(defrule perfil-intermedio
(not (perfil completo))
(or (and (programacion SI)
(or (administracion SI) (tecnologia SI)) (or (redes SI) (redes NO)))
(and (programacion NO)
(and (tecnologia SI) (redes SI) (administracion SI)))
(and (programacion NO)
(and (tecnologia SI) (redes SI)))
(and (tecnologia SI) (administracion SI))
(and (redes SI) (administracion SI)))
=>
(assert (perfil intermedio))
)