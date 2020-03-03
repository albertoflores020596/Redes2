

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

/**
 *
 * @author usuario
 */
public class Cliente {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Scanner sc = new Scanner(System.in);
        int n,m,p;

        System.out.println("Bienvenido a buscaminas");
        System.out.println("¿Seleciona la dificultad?");
        System.out.println("1.Fácil");
        System.out.println("2.Dificil");
        n = sc.nextInt();
        Tablero tab = Tiro(-1, -1, n);

        System.out.println(tab);
        while (tab.getEstadoJuego() == 0) {
            n = 0;
            System.out.println("Ingrese las coordenadas");
            m=sc.nextInt()-1;
            p=sc.nextInt()-1;
            tab = Tiro(m, p, n);
            System.out.println(tab);
        }
        if (tab.getEstadoJuego() == 1) {
            System.out.println("ohhhh,  Eres genial GANASTE");
            tab.destapaT();
            System.out.println(tab);
        } else {
            System.out.println("BUUUUUUUUUUUUUUUU!!!!  Looser");
            tab.destapaT();
            System.out.println(tab);
        }

    }

    public static Tablero Tiro(int x, int y, int jugada) {
        Tablero t = null;
        try {
            // Apertura del socket y los flujos IO
            Socket s = new Socket(InetAddress.getByName("10.100.66.205"), 4040);
            ObjectOutputStream os = new ObjectOutputStream(s.getOutputStream());
            ObjectInputStream is = new ObjectInputStream(s.getInputStream());

            os.flush();

            Jugada j1 = new Jugada();

            j1.setTipo(jugada);
            j1.setX(x);
            j1.setY(y);
            os.writeObject(j1);
            os.flush();

            t = (Tablero) is.readObject();


            //Cerramos los flujos y el socket
            is.close();
            os.close();
            s.close();
        } catch (UnknownHostException ex) {
        } catch (IOException ex) {
        } catch (ClassNotFoundException ex) {
        }
        return t;
    }
}
